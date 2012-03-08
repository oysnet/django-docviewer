from django.core.management.base import BaseCommand
from docviewer.models import Document

from optparse import make_option
from docviewer.helpers import docsplit
from celery.task.control import revoke


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        for d in Document.objects.filter(status = Document.STATUS.waiting):
            
            print "revoke task for %s" % d
            
            revoke(d.task_id)