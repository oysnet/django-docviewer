Demo project for django-docviewer
=================================

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



Installation of the virtual environment:
----------------------------------------

1) Install the packages::

    $ sudo pip install --upgrade pip 
    $ sudo pip install --upgrade virtualenv 
    $ sudo pip install virtualenvwrapper
    
2) Create your .venv directory::

    $ mkdir -p ~/.venvs

3) You need to configure the environment::

    $ export WORKON_HOME=~/.venvs
    $ source /usr/local/bin/virtualenvwrapper.sh

4) Add the lines to your .bashrc file so the next time your environment is ready::

  a) Opent the .bashrc::

        $ pico .bashrc

  b) Opent the .bashrc::

        export WORKON_HOME=~/.venvs
        source /usr/local/bin/virtualenvwrapper.sh

5) Create a virtualenv for the project::

    $ mkvirtualenv docviewer_env --no-site-packages

6) Try it::

    $ workon docviewer_env
    $ deactivate


Installation of the Demo Project:
---------------------------------

1) Start the virtual environment::

    $ workon docviewer_env

2) Go to the folder::

    $ cd path/to/django-docviewer/

3) Run the setup::

    $ python setup.py develop

4) Now go to the folder of the DEMO::

    $ cd path/to/django-docviewer/demo/

5) Run the 2nd setup::

    $ python setup.py develop

6) Got to the demo Root Project::

    $ cd demo/demoproject/

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

    http://localhost:8000/admin/docviewer/document/add/

5) You will need to wait a few seconds while docsplit splits the document and elasticsearch index it. You can see the status in the admin interface. When the status is 'ready', you can search in the following URL (make sure you search with an appropiate term that is insider your pdf)::

    localhost:8000/search/

6) You can also try accessing the document directly::

    Access the document : http://localhost:8000/viewer/1/demo.html
