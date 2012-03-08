from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel, StatusModel
from model_utils import Choices
from autoslug.fields import AutoSlugField
import os, re, codecs

from docviewer.settings import *


RE_PAGE = re.compile(r'^.*_([0-9]+)\.txt')

class Document(TimeStampedModel, StatusModel):
    
    STATUS = Choices('waiting', 'ready', 'running', 'failed')
        
    slug = AutoSlugField(_('Slug'),max_length=255, unique=True, populate_from='title')
    
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    
    source_url = models.URLField(_('Source URL of the document'), max_length=1024, null=True, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    
    contributor = models.CharField(_('Contributor'), max_length=255, null=True, blank=True)
    contributor_organization = models.CharField(_('Contributor organization'), max_length=255, null=True, blank=True)
    
    download = models.BooleanField(default=True)
    
    related_url = models.URLField(max_length=1024, null=True, blank=True)
    
    filename = models.CharField(_('PDF file name'), max_length=512, null=True, blank=True)
    
    task_id = models.CharField(_('Celery task ID'), max_length=50, null=True, blank=True)
    task_error = models.TextField(_('Celery error'), null=True, blank=True)
    
    task_start = models.DateTimeField(_('Celery date start'), null=True, blank=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ("docviewer_viewer_view", (), {'slug' : self.slug, 'pk': self.pk})
    
    
    def __unicode__(self):
        return u"%s %s (status:%s)" % (self.pk, self.title, self.status)
    
    @property
    def text_url(self):
        return "%s/%s.txt" % (self.get_root_url(), self.slug)
    
    @property
    def thumbnail_url(self):
        return "%s/%s.%s" % (self.get_root_url(),  self.slug, IMAGE_FORMAT)
    
    @property
    def doc_url(self):
        return "%s/%s.pdf" % (self.get_root_url(),  self.slug)
    
    @property
    def text_page_url(self):
        return "%s/%s_%%(page)s.txt" % (self.get_root_url(), self.slug)
    
    @property
    def image_page_url(self):
        return "%s/%%(size)s/%s_%%(page)s.%s" % (self.get_root_url(), self.slug, IMAGE_FORMAT)
        
    
        
    def get_root_path(self):
        return "%s%s" % (DOCUMENT_ROOT,self.id)
    
    def get_root_url(self):
        return "%s%s" % (DOCUMENT_URL,self.id)
    
    @property
    def text(self):
        path = "%sall.txt" %( self.document.get_root_path())
        f = open(path, 'r').read()
        data = f.read()
        f.close()
        return data
    
    
    def save(self, *args, **kwargs):
        
        create = self.pk is None
        super(Document, self).save(*args, **kwargs)
        if create:
            os.makedirs(self.get_root_path())
    
    def get_file_path(self):
        return "%s/%s" % (self.get_root_path(), self.filename)
    
    def set_file(self, path):
        
        file = open(path, 'r')
        filepath = "%s/%s.%s" % (self.get_root_path(), self.slug, path.split('.')[-1])
        f = open(filepath, "w")
        f.write(file.read())
        f.close()
        file.close()
        
        self.filename = filepath.split('/')[-1]
        
    
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
       
        
class Page(models.Model):
    " Model used to index pages "
    document = models.ForeignKey(Document, related_name='pages_set')
    page = models.PositiveIntegerField()
    
    @property
    def text(self):
        path = "%s/%s_%s.txt" %( self.document.get_root_path(), self.document.slug, self.page)
        f = codecs.open(path, 'r')
        data = f.read()
        f.close()
        return data.decode('ascii', 'ignore')
        
    
    
    def get_image(self, size):
        return "%s%s/%s.%s" %( self.document.get_root_url(), size, self.page, IMAGE_FORMAT)
        
    
class Section(models.Model):
    document = models.ForeignKey(Document, verbose_name=_('Document'),related_name='sections_set')
    
    title = models.CharField(_('Title'), max_length=255)
    page = models.PositiveIntegerField(_('Page ID'))
    
    
class Annotation(models.Model):
    document = models.ForeignKey(Document, related_name='annotations_set')
    
    title = models.CharField(_('Title'), max_length=255)
    location = models.CommaSeparatedIntegerField(_('Coordinates'), max_length=50)
    page = models.PositiveIntegerField(_('Page ID'))
    content = models.TextField(_('Content'))
    
    