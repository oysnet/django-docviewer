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
                      #'celery-haystack'],
                      'celery-haystack==0.6.2-old'],
    dependency_links = [
        'http://github.com/toastdriven/django-haystack/tarball/6065c8525bea4b9a116c7fa279b9e3e26ac7362f#egg=django-haystack-2.0.0-beta',
        'http://github.com/jezdez/celery-haystack/tarball/795d37450815c680e4f936f2ba2ff77d882dd3a0#egg=celery-haystack-0.6.2-old'
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
