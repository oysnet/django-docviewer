__all__ = ["DOCUMENT_ROOT", "DOCUMENT_URL", "IMAGE_FORMAT"]

from django.conf import settings
DOCUMENT_ROOT = getattr(settings, "DOCVIEWER_DOCUMENT_ROOT", "/docs/")
DOCUMENT_URL = getattr(settings, "DOCVIEWER_DOCUMENT_URL", "/docs/")
DOCUMENT_MEDIAS_HOST = getattr(settings, "DOCUMENT_MEDIAS_HOST", "MEDIA_URL")
IMAGE_FORMAT = getattr(settings, "DOCVIEWER_IMAGE_FORMAT", "png")
HAYSTACK_CONNECTION = getattr(settings, "DOCVIEWER_HAYSTACK_CONNECTION", "default")