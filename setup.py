# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='django-docviewer',
    version='0.1',
    description='documentcloud for django',
    long_description="",
    author='oxys',
    author_email='contact@oxys.net',
    url='https://github.com/oxys-net/django-docviewer',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['django-autoslug',
                      'django-model-utils',
                      'celery',
                      #'django-haystack',
                      'django-haystack>=2.0.0',
                      'django-pipeline'],
    dependency_links = [
        'http://github.com/toastdriven/django-haystack.git@master#egg=django-haystack-2.0.0'
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
