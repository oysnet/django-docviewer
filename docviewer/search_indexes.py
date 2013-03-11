
from haystack import indexes
from docviewer.models import Page


class PageIndex(CelerySearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True)
    document_id =  indexes.IntegerField(model_attr='document__id')
    page = indexes.IntegerField(model_attr="page")
    
    def prepare_text(self, obj):
        return obj.text

    def get_model(self):
        return Page
            
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
