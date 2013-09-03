from django.views.generic.detail import  BaseDetailView
from django.core.urlresolvers import reverse
from docviewer.models import Document, Page
from django.utils.feedgenerator import rfc2822_date
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.sites.models import Site
from django.views.generic.base import View
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from urlparse import urlsplit, urlunsplit
from .settings import HAYSTACK_CONNECTION
def get_absolute_url(request, relative_url):
    
    
    s =  list(urlsplit(relative_url))

    if s[0] not in ['http', 'https']:
        if request.is_secure():
            s[0] = 'https'
        else:
            s[0] = 'http'
        s[1] = request.get_host()
        return urlunsplit(s)

    return relative_url

class SearchDocumentView(View):
    
    def get(self, request, **kwargs):
        
        query = request.GET.get('q')
        
        results = SearchQuerySet().using(HAYSTACK_CONNECTION).models(Page).narrow('document_id:%s' %  kwargs.get('pk')).auto_query(query)
        
        json = {
          'matches' : results.count(),
          'results' : [p.page for p in results],
          'query'   : query
        }
        
        return HttpResponse(simplejson.dumps(json), content_type="application/json")

class JsonDocumentView(BaseDetailView):
    
    model = Document
    
    def get(self, request, **kwargs):
        document = self.get_object()
        
        print request.get_host()

        json = {}
        json['id'] = "doc-%s" % (document.id,)
        json['title'] = document.title
        json['pages'] = document.page_count
        json['description'] = document.description
        
        json['source'] = document.source_url
        json['created_at'] = rfc2822_date(document.created)
        json['updated_at'] = rfc2822_date(document.modified)
        
        json['canonical_url'] = get_absolute_url(request, reverse("docviewer_viewer_view", kwargs = {'pk' : document.pk, 'slug' : document.slug}))
        
        json['contributor'] = document.contributor
        json['contributor_organization'] = document.contributor_organization
        
        json['resources'] = {}
        if document.download is True:
            json['resources']['pdf'] = get_absolute_url(request, document.doc_url)
        json['resources']['text'] = get_absolute_url(request, document.text_url)
        json['resources']['thumbnail'] = get_absolute_url(request, document.thumbnail_url)
        json['resources']['search'] = get_absolute_url(request, reverse("docviewer_search_view", kwargs = {'pk' : document.pk, 'slug' : document.slug})) + '?q={query}'
        json['resources']['print_annotations'] = get_absolute_url(request, reverse("docviewer_printannotations_view", kwargs = {'pk' : document.pk, 'slug' : document.slug}))
        json['resources']['page'] = {}
        json['resources']['page']['text'] = get_absolute_url(request, document.text_page_url % {'page' : '{page}'})
        json['resources']['page']['image'] = get_absolute_url(request, document.image_page_url % {'page' : '{page}', 'size' : '{size}'})
        
        json['resources']['related_article'] = get_absolute_url(request, document.related_url)
        json['resources']['published_url'] = json['canonical_url']
        
        json['sections'] = list(document.sections_set.all().values('title', 'page'))
        
        json['annotations'] = list(document.annotations_set.all().values('location', 'title', 'id', 'page', 'content'))
        
        
        return HttpResponse(simplejson.dumps(json), content_type="application/json")