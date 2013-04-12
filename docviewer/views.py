from django.views.generic.detail import BaseDetailView
from django.core.urlresolvers import reverse
from docviewer.models import Document, Page, Annotation
from django.utils.feedgenerator import rfc2822_date
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.sites.models import Site
from django.views.generic.base import View
from haystack.query import SearchQuerySet

SITE = Site.objects.get_current()


def get_absolute_url(relative_url):
    if relative_url and (relative_url[0:7] == 'http://' or relative_url[0:8] == 'https://'):
        return relative_url
    return "http://%s%s" % (SITE.domain, relative_url)


def update_annotation(request, pk):
    """
    Update an annotation
    """
    annotation = Annotation.objects.get(id=request.GET.get('id'))
    if 'title' in request.GET:
        if (request.GET.get('title').strip()) == "":
            annotation.title = "Untitled"
        else:
            annotation.title = request.GET.get('title')
    if 'content' in request.GET:
        annotation.content = request.GET.get('content')
    annotation.save()
    return HttpResponse(
        simplejson.dumps({'status': 'ok'}), content_type="application/json")


def add_annotation(request, pk):
    """
    Add an annotation
    """
    document = Document.objects.get(pk=pk)
    annotation = Annotation(
        document=document, page=request.GET.get('page_id'))
    if 'title' in request.GET:
        if (request.GET.get('title').strip()) == "":
            annotation.title = "Untitled"
        else:
            annotation.title = request.GET.get('title')
    if 'content' in request.GET:
        annotation.content = request.GET.get('content')
    if 'location' in request.GET:
        annotation.location = request.GET.get('location')
    annotation.save()
    return HttpResponse(
        simplejson.dumps({
            'status': 'ok',
            'url': document.get_absolute_url() + '#document/p' +
            str(document.pk) + '/a' + str(annotation.pk)}),
        content_type="application/json"
    )


def remove_annotation(request, pk):
    """
    Remove an annotation
    """

    annotation = Annotation.objects.get(id=request.GET.get('id'))

    annotation.delete()

    return HttpResponse(simplejson.dumps(
        {'status': 'ok'}), content_type="application/json")


class SearchDocumentView(View):

    def get(self, request, **kwargs):

        query = request.GET.get('q')

        results = SearchQuerySet().models(Page).narrow(
            'document_id:%s' % kwargs.get('pk')).auto_query(query)\
            .order_by('document_id')

        json = {
            'matches': results.count(),
            'results': [p.page for p in results],
            'query': query}

        return HttpResponse(simplejson.dumps(json), content_type="application/json")


class JsonDocumentView(BaseDetailView):

    model = Document

    def get(self, request, **kwargs):
        document = self.get_object()
        json = {}
        json['id'] = "doc-%s" % (document.id,)
        json['title'] = document.title
        json['pages'] = document.page_count
        json['description'] = document.description
        json['source'] = document.source_url
        json['created_at'] = rfc2822_date(document.created)
        json['updated_at'] = rfc2822_date(document.modified)
        json['canonical_url'] = get_absolute_url(reverse(
            "docviewer_viewer_view", kwargs={
            'pk': document.pk, 'slug': document.slug}))
        json['contributor'] = document.contributor
        json['contributor_organization'] = document.contributor_organization
        json['resources'] = {}
        if document.download is True:
            json['resources']['pdf'] = get_absolute_url(document.doc_url)
        json['resources']['text'] = get_absolute_url(document.text_url)
        json['resources']['thumbnail'] = get_absolute_url(document.thumbnail_url)
        json['resources']['search'] = get_absolute_url(
            reverse("docviewer_search_view", kwargs={
                'pk': document.pk, 'slug': document.slug})) + '?q={query}'
        json['resources']['print_annotations'] = get_absolute_url(
            reverse("docviewer_printannotations_view", kwargs={
                'pk': document.pk, 'slug': document.slug}))
        json['resources']['page'] = {}
        json['resources']['page']['text'] = get_absolute_url(
            document.text_page_url % {'page': '{page}'})
        json['resources']['page']['image'] = get_absolute_url(
            document.image_page_url % {'page': '{page}', 'size': '{size}'})
        json['resources']['related_article'] = get_absolute_url(document.related_url)
        json['resources']['published_url'] = json['canonical_url']

        json['sections'] = list(document.sections_set.all().values('title', 'page'))

        json['annotations'] = list(document.annotations_set.all().values('location', 'title', 'id', 'page', 'content'))

        for annotation in json['annotations']:
            annotation['location'] = {"image": annotation['location']}

        return HttpResponse(simplejson.dumps(json), content_type="application/json")
