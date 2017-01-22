#!/usr/bin/env bash
# Extrahieren der Konfiguration

set -o errexit
set -o nounset
set -o pipefail
set -o verbose

PKG_NAME_REGEXP="^Commandline: /usr/bin/apt-get -q -y -o DPkg::Options::=--force-confold -o DPkg::Options::=--force-confdef install (\K(?:(?:[a-z0-9]+[-+\.a-z0-9]*=(?:[0-9]:)?[0-9]+[+\*\.:~a-z0-9]*(?:\-[+\.~0-9a-z]+)?)\s*)+)$"

grep --color=never --only-matching --perl-regexp "${PKG_NAME_REGEXP}" /var/log/apt/history.log | tr " " "\n" > /vagrant/setup/packages.txt
cp --verbose /etc/apache2/conf-available/wsgi.conf /vagrant/setup
cp --verbose /etc/apache2/sites-available/000-default.conf /vagrant/setup
cp --verbose /etc/postgresql/9.5/main/pg_hba.conf /vagrant/setup
tar czvf /vagrant/setup.tar.gz -C /vagrant/setup . -C /vagrant wheelhouse -C /vagrant LICENSE
