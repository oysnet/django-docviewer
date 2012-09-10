import datetime
from haystack import site
from haystack.indexes import *
from docviewer.models import Page


class PageIndex(RealTimeSearchIndex):

    text = CharField(document=True)
    document_id =  IntegerField(model_attr='document__id')
    page = IntegerField(model_attr="page")
    
    def prepare_text(self, obj):
        return obj.text

    def get_model(self):
        return Page
            
    def index_queryset(self):
        return self.get_model().objects.all()

site.register(Page, PageIndex)
