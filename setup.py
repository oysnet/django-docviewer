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
                      'celery-haystack==0.7.1-beta'],
    dependency_links = [
        'http://github.com/toastdriven/django-haystack/tarball/master#egg=django-haystack-2.0.0-beta',
        'http://github.com/FerumFlex/celery-haystack/tarball/master#egg=celery-haystack-0.7.1-beta'
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
