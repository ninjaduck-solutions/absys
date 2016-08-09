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
    'raven': [
        'raven==5.8.1',
    ],
}

requires = [
    'Django==1.10',
    'dj-database-url==0.4.1',
    'django-autofixture==0.12.1',
    'django-braces==1.9.0',
    'django-configurations==2.0',
    'django-crispy-forms==1.6.0',
    'django-extra-views==0.8.0',
    'django-model-utils==2.5.1',
    'envdir==0.7',
    'fake-factory==0.5.7',
    'psycopg2==2.6.1',
    'pytz==2015.7',
    'django-import-export==0.4.5'
]

# Hard linking doesn't work inside VirtualBox shared folders. This means that
# you can't use tox in a directory that is being shared with Vagrant,
# since tox relies on `python setup.py sdist` which uses hard links. As a
# workaround, disable hard-linking if setup.py is a descendant of /vagrant.
# See
# https://stackoverflow.com/questions/7719380/python-setup-py-sdist-error-operation-not-permitted
# for more details.
if os.path.dirname(os.path.abspath(__file__)) == '/vagrant':
    del os.link

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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
