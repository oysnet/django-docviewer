from celery.task import task


@task()
def generate_document(doc_id, filepath, task_id=None):
    from docviewer.helpers import generate_document    
    generate_document(doc_id, filepath, task_id)