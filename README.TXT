django-docview is a fork of document-viewer https://github.com/NYTimes/document-viewer

All dependecies to jammit and ruby have been removed and replaced by django-pipeline
document-viewer was only a client viewer, django-docview store document data and generate data using docsplit (https://github.com/documentcloud/docsplit) and celery.

Please read original licences in docviewer directory