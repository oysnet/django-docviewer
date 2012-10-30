from django.conf import settings
import haystack
from docviewer.models import Page

if haystack.__version__[0] == 2:
	from haystack import indexes

	class PageIndex(indexes.SearchIndex, indexes.Indexable):
		text = indexes.CharField(document=True, use_template=True)
		document_id =  indexes.IntegerField(model_attr='document__id')
		page = indexes.IntegerField(model_attr="page")
		
		def prepare_text(self, obj):
		    return obj.text

		def get_model(self):
		    return Page
		        
		def index_queryset(self):
		    return self.get_model().objects.all()

else:
	from haystack import site
	from haystack.indexes import *

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
