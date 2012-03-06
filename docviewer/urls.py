from django.conf.urls.defaults import patterns, include, url
from docviewer.views import JsonDocumentView

urlpatterns = patterns('',
    (r'^(?P<pk>\d+)/(?P<slug>.+)\.json$', JsonDocumentView.as_view(), {}, "docviewer_json_view"),
    (r'^(?P<pk>\d+)/(?P<slug>.+)\.html$', JsonDocumentView.as_view(), {}, "docviewer_viewer_view"),
    (r'^search/(?P<pk>\d+)/(?P<slug>.+)\.json$', JsonDocumentView.as_view(), {}, "docviewer_search_view"),
    (r'^print-annotations/(?P<pk>\d+)/(?P<slug>.+)\.html$', JsonDocumentView.as_view(), {}, "docviewer_printannotations_view"),
)
