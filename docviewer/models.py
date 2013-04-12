from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from model_utils.models import TimeStampedModel, StatusModel
from model_utils import Choices
from autoslug.fields import AutoSlugField
import os
import re
import codecs
import shutil
import uuid

from docviewer.settings import IMAGE_FORMAT, DOCUMENT_ROOT, DOCUMENT_URL
from docviewer.tasks import task_generate_document


RE_PAGE = re.compile(r'^.*_([0-9]+)\.txt')


class Document(TimeStampedModel, StatusModel):

    STATUS = Choices('waiting', 'ready', 'running', 'failed')
    LANGUAGES = Choices(
        ("eng","English"),
        ("spa","Spanish"),
        ("spa_old","Old Spanish"))

    slug = AutoSlugField(
        _('Slug'), max_length=255, unique=True, populate_from='title')
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    source_url = models.URLField(
        _('Source URL of the document'), max_length=1024, null=True,
        blank=True)
    language = models.CharField(_('Language'), choices=LANGUAGES,
        default='spa', max_length=7, null=False, blank=False)
    page_count = models.PositiveIntegerField(
        null=True, blank=True, help_text=_('Total page in the document'))
    contributor = models.CharField(
        _('Contributor'), max_length=255, null=True, blank=True)
    contributor_organization = models.CharField(
        _('Contributor organization'),
        max_length=255, null=True, blank=True)
    download = models.BooleanField(
        _('Allow download'), default=True,
        help_text=_('Allow original document download'))
    related_url = models.URLField(
        _('Url where the document can be view'),
        max_length=1024, null=False, blank=True, default='')
    docfile = models.FileField(
        _('PDF Document File'), upload_to='pdfs/%Y/%m/%d', max_length=512,
        null=False, blank =False)
    task_id = models.CharField(
        _('Celery task ID'), max_length=50, null=True, blank=True)
    task_error = models.TextField(
        _('Celery error'), null=True, blank=True)
    task_start = models.DateTimeField(
        _('Celery date start'), null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ("docviewer_viewer_view", (), {
            'slug': self.slug, 'pk': self.pk})

    def __unicode__(self):
        return u"%s %s (status:%s)" % (self.pk, self.title, self.status)

    @property
    def text_url(self):
        return "%s/%s.txt" % (self.get_root_url(), self.slug)

    @property
    def thumbnail_url(self):
        return "%s/small/%s_1.%s" % (
            self.get_root_url(), self.slug, IMAGE_FORMAT)

    @property
    def doc_url(self):
        return "%s/%s.pdf" % (self.get_root_url(), self.slug)

    @property
    def text_page_url(self):
        return "%s/%s_%%(page)s.txt" % (self.get_root_url(), self.slug)

    @property
    def image_page_url(self):
        return "%s/%%(size)s/%s_%%(page)s.%s" % (
            self.get_root_url(), self.slug, IMAGE_FORMAT)

    def get_root_path(self):
        return "%s%s" % (DOCUMENT_ROOT, self.id)

    def get_root_url(self):
        return "%s%s" % (DOCUMENT_URL, self.id)

    @property
    def text(self):
        f = open(self.text_url, 'r')
        data = f.read()
        f.close()
        return data

#    def save(self, *args, **kwargs):
#        create = self.pk is None
#        super(Document, self).save(*args, **kwargs)
#        if create:
#            os.makedirs(self.get_root_path())
#            self.process_file()

    def get_file_path(self):
        return "%s/%s" % (self.get_root_path(), self.docfile_basename)

    def process_file(self):
        file = open(os.path.join(settings.MEDIA_ROOT,self.docfile.name), 'r')
        filepath = "%s/%s.%s" % (
            self.get_root_path(), self.slug,
            self.docfile_basename.split('.')[-1].lower())
        f = open(filepath, "w")
        f.write(file.read())
        f.close()
        file.close()

        self.title = self.docfile_basename
        task = task_generate_document.apply_async(args=[self.pk], countdown=5)
        self.task_id = task.task_id
        self.save()

    @property
    def docfile_basename(self):
        return os.path.basename(self.docfile.name)

    def generate(self):
        # concatenate all text files
        all_txt = open("%s/%s.txt" % (self.get_root_path(), self.slug), "w")
        self.page_count = 0
        self.pages_set.all().delete()
        for f in os.listdir(self.get_root_path()):
            if f[-4:] == '.txt' and f != "%s.txt" % self.slug:
                self.page_count += 1
                tmp_file = open("%s/%s" % (self.get_root_path(), f))
                all_txt.write(tmp_file.read())
                Page(document=self, page=RE_PAGE.match(f).group(1)).save()
                tmp_file.close()
        all_txt.close()

    def get_thumbnail(self):
        return "%s/%s/%s_%s.%s" % (
            self.get_root_url(), "small", self.slug, 1, IMAGE_FORMAT)

    class Meta:
        verbose_name = _(u'Document')
        verbose_name_plural = _(u'Document')


class Page(models.Model):
    " Model used to index pages "
    document = models.ForeignKey(Document, related_name='pages_set')
    page = models.PositiveIntegerField()

    @property
    def text(self):
        path = "%s/%s_%s.txt" % (
            self.document.get_root_path(), self.document.slug, self.page)
        f = codecs.open(path, 'r')
        data = f.read()
        f.close()
        return data.decode('ascii', 'ignore')

    def get_image(self, size):
        return "%s/%s/%s_%s.%s" % (
            self.document.get_root_url(), size, self.document.slug,
            self.page, IMAGE_FORMAT)

    def get_thumbnail(self):
        return self.get_image("small")


class Section(models.Model):
    document = models.ForeignKey(
        Document, verbose_name=_('Document'), related_name='sections_set')
    title = models.CharField(_('Title'), max_length=255)
    page = models.PositiveIntegerField(_('Page ID'))


class Annotation(models.Model):
    document = models.ForeignKey(Document, related_name='annotations_set')
    title = models.CharField(_('Title'), max_length=255)
    location = models.CommaSeparatedIntegerField(_('Coordinates'), max_length=50)
    page = models.PositiveIntegerField(_('Page ID'))
    content = models.TextField(_('Content'))


from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver

@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    shutil.rmtree(instance.get_root_path(), ignore_errors=True)
    instance.docfile.delete(False)

#receiver(post_save, sender=Document)
def document_save(sender, instance, created, **kwargs):
    if created and issubclass(sender, Document):
        os.makedirs(instance.get_root_path())
        instance.process_file()

post_save.connect(document_save, dispatch_uid=str(uuid.uuid1()))
