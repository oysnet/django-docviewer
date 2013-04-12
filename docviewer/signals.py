
import shutil
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from models import Document


@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    shutil.rmtree(instance.get_root_path(), ignore_errors=True)
    instance.docfile.delete(False)

@receiver(post_save, sender=Document)
def document_post_save(sender, instance, created, **kwargs):
    print "this is never called"
    if created:
        os.makedirs(instance.get_root_path())
        instance.process_file()
