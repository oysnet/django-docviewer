from django.core.management.base import BaseCommand
from docviewer.models import Document
from docviewer.tasks import task_generate_document



class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        doc = Document.objects.get(pk=args[0])
        task = task_generate_document.apply_async(args=[doc.pk], countdown=5)
        
        doc.status = Document.STATUS.waiting
        doc.task_start = None
        doc.task_id = task.task_id
        doc.save()
        