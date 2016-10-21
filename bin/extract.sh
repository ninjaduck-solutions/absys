#!/usr/bin/env bash
# Extrahieren der Konfiguration

set -o errexit
set -o nounset
set -o pipefail
set -o verbose

PKG_NAME_REGEXP="^Commandline: /usr/bin/apt-get -q -y -o DPkg::Options::=--force-confold -o DPkg::Options::=--force-confdef install (\K[a-z0-9]+[-+\.a-z0-9]+)$"

echo -n > /vagrant/setup/packages.txt
PKGS=$(grep --color=never --only-matching --perl-regexp "${PKG_NAME_REGEXP}" /var/log/apt/history.log | sort)
for PKG in ${PKGS} ;
    do dpkg --status ${PKG} | grep 'Version' | echo "${PKG}=$(cut -c 10-)" >> /vagrant/setup/packages.txt ;
done
cp --verbose /etc/apache2/conf-available/wsgi.conf /vagrant/setup
cp --verbose /etc/apache2/sites-available/django.conf /vagrant/setup
cp --verbose /etc/postgresql/9.5/main/pg_hba.conf /vagrant/setup
tar czvf /vagrant/setup.tar.gz -C /vagrant/setup $(ls -1 /vagrant/setup)
