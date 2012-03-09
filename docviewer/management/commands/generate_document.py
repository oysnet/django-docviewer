from django.core.management.base import BaseCommand
from docviewer.models import Document

from optparse import make_option
from docviewer.helpers import docsplit, generate_document


class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option( '--task',
            action='store',
            dest='task_id',
            default=None,
            help='Celery task ID'),
       )
    
    def handle(self, *args, **options):
        
        for id in args:
            generate_document(id)