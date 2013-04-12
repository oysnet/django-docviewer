import uuid
import shutil
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from models import Document


@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    shutil.rmtree(instance.get_root_path(), ignore_errors=True)
    instance.docfile.delete(False)

#receiver(post_save, sender=Document)
def document_save(sender, instance, created, **kwargs):
    if created and issubclass(sender, Document):
        os.makedirs(instance.get_root_path())
        instance.process_file()

post_save.connect(document_save, dispatch_uid=str(uuid.uuid1()))
