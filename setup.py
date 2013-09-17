# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='django-docviewer',
    version='0.4',
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
                      'django-haystack',
                      'django-pipeline'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
