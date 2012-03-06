from django.views.generic.detail import  BaseDetailView
from django.core.urlresolvers import reverse
from docviewer.models import Document
from django.utils.feedgenerator import rfc2822_date

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
        json['resources']['page']['text'] = reverse("docviewer_pagetext_view", kwargs = {'pk' : document.pk, 'page':'{page}'})
        json['resources']['page']['image'] = reverse("docviewer_pageimage_view", kwargs = {'pk' : document.pk, 'page':'{page}'})