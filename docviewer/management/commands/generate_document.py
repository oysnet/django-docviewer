from django.core.management.base import BaseCommand
from docviewer.models import Document

from optparse import make_option
from docviewer.helpers import docsplit


class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option( '--task',
            action='store',
            dest='task_id',
            default=None,
            help='Celery task ID'),
        make_option('--file',
            action='store',
            dest='filepath',
            default=None,
            help='full file path'),)
    
    def handle(self, *args, **options):
        
        document = Document.objects.get(pk=args[0])
        
        if options.get('task_id', None) is not None and document.task_id != options.get('task_id'):
            raise Exception("Celery task ID doesn't match")
        try:
            docsplit(options.get('filepath'))
        
            document.generate()
            document.status = document.STATUS.ready
            document.task_id = None
            document.save()
        except Exception, e:
            
            try:
                document.task_error = str(e)
                document.save()
            except:
                pass
            
            raise