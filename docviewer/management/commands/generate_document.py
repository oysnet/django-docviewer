from django.core.management.base import BaseCommand
from docviewer.models import Document


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        Document.objects.get(pk=args[0]).generate()