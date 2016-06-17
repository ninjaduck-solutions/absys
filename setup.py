#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from codecs import open

from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read(*paths):
    """Build a file path from *paths and return the contents."""
    with open(os.path.join(*paths), 'r', 'utf-8') as f:
        return f.read()

extras_require = {
    'mailgun': [
        'django-mailgun==0.8.0',
    ],
    'raven': [
        'raven==5.8.1',
    ],
}

requires = [
    'Django==1.8.7',
    'dj-database-url==0.3.0',
    'django-braces==1.8.1',
    'django-configurations==1.0',
    'django-crispy-forms==1.5.2',
    'django-grappelli==2.7.2',
    'django-model-utils==2.4',
    'envdir==0.7',
    'psycopg2==2.6.1',
    'pytz==2015.7',
]

setup(
    name='absys',
    version='0.1.0',
    description='Abrechnungssystem der SLSH und LZH.',
    long_description=read(BASE_DIR, 'README.rst'),
    author='IMTB',
    author_email='noreply@example.com',
    packages=find_packages(),
    include_package_data=True,
    scripts=['manage.py'],
    install_requires=requires,
    license='TBD',
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
