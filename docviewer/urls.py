from django.conf.urls.defaults import patterns, include, url
from docviewer.views import JsonDocumentView, SearchDocumentView
from django.views.generic import DetailView
from docviewer.models import Document
urlpatterns = patterns('',
    (r'^doc-(?P<pk>\d+)\.json$', JsonDocumentView.as_view(), {}, "docviewer_json_view"),
    (r'^(?P<pk>\d+)/(?P<slug>.+)\.html$', DetailView.as_view(context_object_name='document',model=Document), {}, "docviewer_viewer_view"),
    (r'^search/(?P<pk>\d+)/(?P<slug>.+)\.json$', SearchDocumentView.as_view(), {}, "docviewer_search_view"),
    (r'^print-annotations/(?P<pk>\d+)/(?P<slug>.+)\.html$', JsonDocumentView.as_view(), {}, "docviewer_printannotations_view"),
    (r'^(?P<pk>\d+)/update_annotation/$', 'docviewer.views.update_annotation', {}, "docviewer_annotation"),
)
