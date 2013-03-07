# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='django-docviewer',
    version='0.1',
    description='documentcloud for django',
    long_description="",
    author='robertour',
    author_email='robertour@gmail.com',
    url='https://github.com/robertour/django-docviewer',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['django-autoslug',
                      'django-model-utils',
                      'celery',
                      #'django-haystack',
                      'django-haystack==2.0.0-beta',
                      'django-pipeline',
                      #'django-celery',
                      'django-celery',
                      'celery-haystack'],
                      #'celery-haystack==2.0.0-stefanw'],
    dependency_links = [
        'http://github.com/toastdriven/django-haystack/tarball/c5e0ce5221fc97f6a9a6fd9d6b6fad6aec960842#egg=django-haystack-2.0.0-beta'
        #'http://github.com/stefanw/celery-haystack/tarball/signal-processor#egg=celery-haystack-2.0.0-stefanw'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
