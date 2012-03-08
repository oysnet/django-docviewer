import datetime
from haystack.indexes import RealTimeSearchIndex, CharField, IntegerField
from haystack import site
from docviewer.models import Page


class PageIndex(RealTimeSearchIndex):
    
    text = CharField(document=True)
    document_id =  IntegerField(model_attr='document__id')
    page = IntegerField(model_attr="page")
    
    
    def prepare_fulltext(self, obj):
        return obj.text
        
    def index_queryset(self):
        return Page.objects.all()
        
site.register(Page, PageIndex)
