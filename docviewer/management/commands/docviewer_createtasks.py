from django.core.management.base import BaseCommand
from docviewer.models import Document
from docviewer.tasks import task_generate_document
from optparse import make_option



class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option( '--status',
            action='store',
            dest='status',
            default=None,
            help='create a new task for each document that have the specified status'),)
    
    def handle(self, *args, **options):
        
        if options.get('status') is not None:
            docs = Document.objects.filter(status = options.get('status'))
        else:
            docs = Document.objects.filter(pk__in=args)
        
        for doc in docs: 
            
            task = task_generate_document.apply_async(args=[doc.pk], countdown=5)
            
            print "create task for %s" % doc
            
            doc.status = Document.STATUS.waiting
            doc.task_start = None
            doc.task_id = task.task_id
            doc.save()
        