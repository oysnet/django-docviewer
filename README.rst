Django-docviewer for Elasticsearch and Haystack 2.0:
====================================================

This django-docview is a fork of document-viewer https://github.com/oxys-net/django-docviewer which is also a fork of https://github.com/NYTimes/document-viewer. In the oxys-net fork All dependecies to jammit and ruby have been removed and replaced by django-pipeline document-viewer was only a client viewer, django-docview store document data and generate data using docsplit (https://github.com/documentcloud/docsplit) and celery.

There are two reason of this fork to exist:
    1. Support to elasticsearch. This means that I have to configure this django-viewer with the beta haystack(soon the stable release)
    2. Automatic indexing. In the oxys-net fork, it was necessary to rebuild_index or update_index manually (python manage update_index). So, I included the library celery-haystack

Summary of the changes:
-----------------------

- Haystack 2.0.0-beta : included and configured in search_indexes.py
- celery-haystack     : included and configured in search_indexes.py
- django-celery       : easy starting of the celery servery inside the django environment (python manage.py celery worker)
- pyelasticsearch     : included in the installation of the demo (instead of Whoosh)
- elasticsearch       : configured in the settings of the demo
- docviewer           : minor bugs that affects the process of inherit from the main model (document)

Please read original licences in docviewer directory.


Installation of system dependencies:
------------------------------------

1) Install all the packages (the next line has been tried only in Ubuntu 12.04 64b and 12.10 64b)::

    $ sudo apt-get install rabbitmq-server rubygems graphicsmagick poppler-utils pdftk ghostscript tesseract-ocr yui-compressor git python-pip python-dev build-essential npm openjdk-7-jre -y

2) You need to install docsplit:

    a) Install::

        $ sudo gem install docsplit

    b) Try it::

        $ docsplit

    c) This is part of the oxys-net/django-docviewer configuration::

        $ sudo ln -s /usr/local/bin/docsplit /usr/bin/docsplit
        $ sudo ln -s /usr/bin/yui-compressor /usr/local/bin/yuicompressor

3) Install yuglify (need it for production)::

    npm install yuglify

4) Install the elasticsearch::
  
    $ cd ~
    $ wget https://github.com/downloads/elasticsearch/elasticsearch/elasticsearch-0.19.11.deb
    $ sudo dpkg -i elasticsearch-0.19.11.deb

Install the django-docviewer:
-----------------------------

1) Run the following in pip (inside your virtualenv)::

    $ pip install -e git+git://github.com/robertour/django-docviewer.git#egg=django-docviewer

2) Add the following apps to the INSTALLED_APPS of your Django settings::

    'pipeline',        # necessary for compression and docviewer templates
    'djcelery',        # necessary for python manage.py celery worker
    'celery_haystack', # necessary for automatic rebuild_index
    'haystack',        # necessary for manual rebuild_index
    'docviewer',

3) Add the pipeline configuration to your Django settings::

    # Pipeline configuration
    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
    PIPELINE = False
    PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
    PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'

4) Add the celery configuration to your Django settings::

    # Celery configuration
    BROKER_URL='amqp://guest:guest@localhost:5672//'

5) Add the haystack configuration to your Django settings::
    #Haystack configuration

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }


6) Add the docviewer configuration to your Django settings (decide your directories)::

    # Docviewer Configuration
    from os.path import join
    #PROJECT_ROOT is my actual path to the project. You may have to change this a bit
    DOCVIEWER_DOCUMENT_ROOT = join(PROJECT_ROOT,'docs/') 
    DOCVIEWER_DOCUMENT_URL = '/docs/'
    DOCVIEWER_IMAGE_FORMAT =  'png'


7) Update your database and launch:

    a) Update database::

        $ python manage.py syncdb

    b) Launch your site::

        $ python manage.py runserver localhost:8000

    c) Access the site in the URL http://localhost:8000/admin/

    d) Logging with the user created in syncdb or any other admin

    e) Go to the following address::

        localhost:8000/admin/sites/site/1/

    f) Check the domain name is correct ("localhost:8000" if you are developing). Or change it to the your real domain name. This is mandatory for the docviewer to find the images of your pdfs. You will need to restart the server::
        $ python manage.py runserver localhost:8000


Testing the installation:
-------------------------

1) Start the server::

    $ python manage.py runserver localhost:8000

3) In another terminal run the celery service::

    $ python manage.py celery worker

4) Add a scanned pdf document (for convenience, there is one in ~/git/django-docviewer/test.pdf) through the admin interface::

    localhost:8000/admin/document/

5) You will need to wait a few seconds while docsplit splits the document and elasticsearch index it. You can see the status in the admin interface. When the status is 'ready', you can search in the following URL (make sure you search with an appropiate term that is insider your pdf)::

    localhost:8000/search/

6) You can also try accessing the document directly::

    Access the document : http://localhost:8000/viewer/1/demo.html


Disabling stop words:
---------------------

1) Open the elasticsearch.yml::

    $ sudo nano /etc/elasticsearch/elasticsearch.yml

2) Add the following to the configuration file (in the Index section)

    index:
      analysis:
        analyzer:
        # set standard analyzer with no stop words as the default for both indexing and searching
        default:
            type: standard
            stopwords: _none_

3) Restart the elasticsearch service::

    sudo service elasticsearch restart
