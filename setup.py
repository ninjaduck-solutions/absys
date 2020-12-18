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
}

requires = [
    'arrow',
    'Django==2.2.*',
    'dj-database-url',
    'django-autofixture',
    'django-braces',
    'django-configurations',
    'django-crispy-forms',
    'django-extra-views',
    'django-filter',
    'django-lockdown',
    'django-model-utils',
    'django-weasyprint==0.5.3',
    # For weasyprint
    #'docutil',
    'envdir',
    'Faker',
    'psycopg2-binary',
    'pytz',
    'django-import-export',
    'django-wkhtmltopdf',
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
    version='1.3.0',
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
        'License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
