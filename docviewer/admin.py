from django.contrib import admin
from docviewer.models import Document, Annotation
from docviewer.forms import DocumentForm
from django.contrib.admin.views.main import ChangeList


class DocViewerChangeList(ChangeList):
    def __init__(self, request, *args, **kwargs):
        params = dict(request.GET.items())
        try:
            del params['CKEditorFuncNum']
        except:
            pass
        request.GET = params
        super(DocViewerChangeList, self).__init__(request, *args, **kwargs)


class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm
    readonly_fields = ('status', 'page_count', 'task_id', 'task_error', 'task_start')

    fieldsets = (
        (None, {'fields': (
            'title', 'description', 'docfile', 'language', 'source_url',
            'related_url', 'contributor', 'contributor_organization',
            'download')}),
        ('Meta', {'fields': (
            'status', 'page_count',
            'task_id', 'task_error', 'task_start')}),
    )

    def get_changelist(self, request, **kwargs):
        return DocViewerChangeList

admin.site.register(Document, DocumentAdmin)
admin.site.register(Annotation)
