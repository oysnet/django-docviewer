from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

DOCUMENT_ROOT = getattr(settings, "DOCVIEWER_DOCUMENT_ROOT", "documents/")
MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
IMAGE_FORMAT = getattr(settings, "DOCVIEWER_IMAGE_FORMAT", "gif")

class Document(models.Model):
    
    created = models.DateTimeField(_('Creation date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Last update date'), auto_now=True, editable=False)
    
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    
    source_url=models.URLField(_('Source URL of the document'), max_length=1024, null=True, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    
    contributor = models.CharField(_('Contributor'), max_length=255, null=True, blank=True)
    contributor_organization = models.CharField(_('Contributor organization'), max_length=255, null=True, blank=True)
    
    file = models.FileField(upload_to="%s/%%Y/%%m/" % DOCUMENT_ROOT)
        
    @property
    def text_url(self):
        return "%s.txt" % self.get_root_url()
    
    @property
    def thumbnail_url(self):
        return "%s.%s" % (self.get_root_url(), IMAGE_FORMAT)
    
    @property
    def text_page_url(self):
        return "%s_%%(page)s.txt" % self.get_root_url()
    
    @property
    def image_page_url(self):
        return "%s/%%(size)s/%s_%%(page)s.%s" % (self.get_root_url(), self.pk, IMAGE_FORMAT)
        
    
        
    def get_root_path(self):
        return "%s%s" % (MEDIA_ROOT, self.id)
    
    def get_root_url(self):
        return "%s%s" % (MEDIA_URL, self.id)
    
    @property
    def text(self):
        path = "%sall.txt" %( self.document.get_root_path())
        f = open(path, 'r').read()
        data = f.read()
        f.close()
        return data
    
class Page(models.Model):
    " Model used to index pages "
    document = models.ForeignKey(Document, related_name='pages_set')
    page = models.PositiveIntegerField()
    
    @property
    def text(self):
        path = "%s%s.txt" %( self.document.get_root_path(), self.page)
        f = open(path, 'r').read()
        data = f.read()
        f.close()
        return data
    
    
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
    
    