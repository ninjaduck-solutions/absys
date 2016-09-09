#!/usr/bin/env bash
# Extrahieren der Konfiguration

set -o errexit
set -o nounset
set -o pipefail
set -o verbose

dpkg --list > /vagrant/setup/packages.txt
cp --verbose /var/log/apt/history.log /vagrant/setup
cp --verbose /etc/apache2/conf-available/wsgi.conf /vagrant/setup
cp --verbose /etc/apache2/sites-available/django.conf /vagrant/setup
cp --verbose /etc/postgresql/9.5/main/pg_hba.conf /vagrant/setup
