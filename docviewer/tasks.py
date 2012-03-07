from celery.task import task
from django.core import management
from docviewer.models import Document
from docviewer.helpers import docsplit

@task()
def generate_document(doc_id, filepath, task_id=None):
    
    document = Document.objects.get(pk=doc_id)
        
    if document.task_id != task_id:
        
        raise Exception("Celery task ID doesn't match")
    try:
        docsplit(filepath)
    
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