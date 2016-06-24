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
    'Django==1.8.7',
    'dj-database-url==0.3.0',
    'django-autofixture==0.12.1',
    'django-braces==1.8.1',
    'django-configurations==1.0',
    'django-crispy-forms==1.5.2',
    'django-extra-views==0.8.0',
    'django-grappelli==2.7.2',
    'django-model-utils==2.4',
    'envdir==0.7',
    'fake-factory==0.5.7',
    'psycopg2==2.6.1',
    'pytz==2015.7',
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
