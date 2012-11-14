
This django-docview is a fork of document-viewer https://github.com/oxys-net/django-docviewer which is also a fork of https://github.com/NYTimes/document-viewer

In the oxys-net fork All dependecies to jammit and ruby have been removed and replaced by django-pipeline document-viewer was only a client viewer, django-docview store document data and generate data using docsplit (https://github.com/documentcloud/docsplit) and celery.

There are two reason of this fork to exist:
    1. Support to elasticsearch. This means that I have to configure this django-viewer with the beta haystack(soon the stable release)
    2. Automatic indexing. In the oxys-net fork, it was necessary to rebuild_index or update_index manually (python manage update_index). So, I included the library celery-haystack

Summary of the changes:
- Haystack 2.0.0-beta : included and configured in search_indexes.py
- celery-haystack     : included and configured in search_indexes.py
- django-celery       : easy starting of the celery servery inside the django environment (python manage.py celery worker)
- pyelasticsearch     : included in the installation of the demo (instead of Whoosh)
- elasticsearch       : configured in the settings of the demo
- docviewer           : minor bugs that affects the process of inherit from the main model (document)

Please read original licences in docviewer directory