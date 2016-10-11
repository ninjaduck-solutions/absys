#!/usr/bin/env bash
# Extrahieren der Konfiguration

set -o errexit
set -o nounset
set -o pipefail
set -o verbose

grep --color=never --only-matching --perl-regexp "^Commandline: /usr/bin/apt-get -q -y -o DPkg::Options::=--force-confold -o DPkg::Options::=--force-confdef install (\K[a-z0-9]+[-+\.a-z0-9]+)$" /var/log/apt/history.log | sort > /vagrant/setup/packages.txt
cp --verbose /etc/apache2/conf-available/wsgi.conf /vagrant/setup
cp --verbose /etc/apache2/sites-available/django.conf /vagrant/setup
cp --verbose /etc/postgresql/9.5/main/pg_hba.conf /vagrant/setup
