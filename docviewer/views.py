from django.views.generic.detail import  BaseDetailView
from django.core.urlresolvers import reverse
from docviewer.models import Document
from django.utils.feedgenerator import rfc2822_date
from django.http import HttpResponse
from django.utils import simplejson

class JsonDocumentView(BaseDetailView):
    
    model = Document
    
    def get(self, request, **kwargs):
        document = self.get_object()
        
        
        json = {}
        json['id'] = str(document.id)
        json['title'] = document.title
        json['pages'] = document.page_count
        json['description'] = document.description
        
        json['source'] = document.source_url
        json['created_at'] = rfc2822_date(document.created)
        json['updated_at'] = rfc2822_date(document.modified)
        
        json['canonical_url'] = reverse("docviewer_viewer_view", kwargs = {'pk' : document.pk})
        
        json['contributor'] = document.contributor
        json['contributor_organization'] = document.contributor_organization
        
        json['resources'] = {}
        json['resources']['pdf'] = document.file.url
        json['resources']['text'] = document.text_url
        json['resources']['thumbnail'] = document.thumbnail_url
        json['resources']['search'] = reverse("docviewer_search_view", kwargs = {'pk' : document.pk})
        json['resources']['print_annotations'] = reverse("docviewer_printannotations_view", kwargs = {'pk' : document.pk})
        json['resources']['page'] = {}
        json['resources']['page']['text'] = document.text_page_url % {'page' : '{page}'}
        json['resources']['page']['image'] = document.image_page_url % {'page' : '{page}', 'size' : '{size}'}
        
        json['resources']['related_article'] = ""
        json['resources']['published_url'] = json['canonical_url']
        
        json['sections'] = list(document.sections_set.all().values('title', 'page'))
        
        json['annotations'] = list(document.annotations_set.all().values('location', 'title', 'id', 'page', 'content'))
        
        
        return HttpResponse(simplejson.dumps(json), content_type="application/json")