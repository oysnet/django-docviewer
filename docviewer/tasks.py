from celery.task import task


@task()
def task_generate_document(doc_id, task_id=None):
    from docviewer.helpers import generate_document    
    generate_document(doc_id, task_id)