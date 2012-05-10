from django.contrib import admin
from docviewer.models import Document
from docviewer.forms import DocumentForm
from docviewer.tasks import task_generate_document



class DocumentAdmin(admin.ModelAdmin):
    
    form = DocumentForm
    readonly_fields = ('status', 'page_count', 'filename', 'task_id', 'task_error', 'task_start')
    
    fieldsets = (
        (None, {'fields': ('title', 'description', 'file', 'source_url', 'related_url', 'contributor', 'contributor_organization', 'download')}),
        ('Meta', {'fields': ('status', 'filename', 'page_count',  'task_id', 'task_error', 'task_start')}),
    )
    
    def save_model(self, request, obj, form, change):
        obj.save()
        file = form.cleaned_data['file']
        obj.set_file(file = file, filename=file.name)
        
admin.site.register(Document, DocumentAdmin)