from celery.decorators import task
from django.core import management

@task()
def generate_document(doc_id, filepath, task_id=None):
    management.call_command('generate_document', doc_id, file=filepath, task=task_id, verbosity=0, interactive=False)