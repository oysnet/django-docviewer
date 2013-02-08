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
    readonly_fields = ('status', 'page_count', 'filename', 'task_id', 'task_error', 'task_start')

    fieldsets = (
        (None, {'fields': (
            'title', 'description', 'file', 'source_url', 'related_url',
            'contributor', 'contributor_organization', 'download')}),
        ('Meta', {'fields': (
            'status', 'filename', 'page_count',
            'task_id', 'task_error', 'task_start')}),
    )

    def get_changelist(self, request, **kwargs):
        return DocViewerChangeList

    def save_model(self, request, obj, form, change):
        obj.save()
        file = form.cleaned_data['file']
        obj.set_file(file=file, filename=file.name)

admin.site.register(Document, DocumentAdmin)
admin.site.register(Annotation)
