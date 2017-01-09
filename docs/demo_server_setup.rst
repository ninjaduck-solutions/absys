*****************
Demo Server Setup
*****************

Sowohl für das Setup als auch das Upgrade müssen vorher in der dev Vagrant Box
alle Python Wheels gesammelt werden:

::

    (pyvenv) vagrant@absys-dev:/vagrant$ make dist
    (pyvenv) vagrant@absys-dev:/vagrant$ make wheelhouse

.. note::

    Das ``absys`` Paket sollte am besten aus einem Release erstellt werden.
    Dieser kann mit ``git checkout 1.0.0`` wiederhergestellt werden, wobei
    "1.0.0" mit der gewünschten Version zu ersetzen ist. Nach dem Erstellen der
    Python Wheels wieder den Entwicklungsbranch mit ``git checkout develop``
    herstellen.

Setup
=====

Zum Setup eines Demo Servers wie folgt vorgehen:

::

    $ ssh root@absys-demo "mkdir -p /var/wheelhouse-archive"
    $ ssh root@absys-demo "chmod --verbose o+rX /var/wheelhouse-archive"
    $ scp -r wheelhouse root@absys-demo:/var/wheelhouse-archive/wheelhouse-$(date "+%Y-%m-%d")
    $ ssh root@absys-demo
    root:~$ locale-gen en_US.UTF-8
    root:~$ wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
    root:~$ echo "deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main" > /etc/apt/sources.list.d/saltstack.list
    root:~$ apt-get update
    root:~$ apt-get --yes install git salt-minion
    root:~$ adduser --disabled-password --gecos "" vagrant
    root:~$ echo "vagrant ALL = NOPASSWD: ALL" >> /etc/sudoers
    root:~$ rm /var/wheelhouse
    root:~$ ln -s /var/wheelhouse-archive/wheelhouse-$(date "+%Y-%m-%d") /var/wheelhouse
    root:~$ su -l vagrant
    vagrant:~$ git clone ssh://git@h2516835.stratoserver.net:2050/srv/git/absys.git
    vagrant:~$ cd absys
    vagrant:absys$ git checkout <release_version>
    vagrant:absys$ sudo salt-call --local --file-root=salt/roots/salt --pillar-root=salt/roots/pillar state.apply
    vagrant:absys$ sudo salt-call --local --file-root=salt/roots/salt --pillar-root=salt/roots/pillar state.apply apache
    vagrant:absys$ sed -i 's/PACKAGE_PATH=.*/PACKAGE_PATH=\/var\/wheelhouse/' setup/install.sh
    vagrant:absys$ ./setup/install.sh
    vagrant:absys$ git checkout master
    vagrant:absys$ exit
    root:~$ exit

PostgreSQL Backup
=================

Falls nötig, kann jederzeit ein PostgreSQL Backup erstellt werden.

Backup erstellen
----------------

::

    $ ssh root@absys-demo
    root:~$ mkdir -p /var/backups/pg_dump
    root:~$ chown --verbose postgres: /var/backups/pg_dump
    root:~$ sudo --user postgres --login
    postgres:~$ pg_dump --format=custom --username=absys absys > /var/backups/pg_dump/absys_$(date --iso-8601=seconds).dump
    postgres:~$ exit
    root:~$ exit

Backup wiederherstellen
-----------------------

::

    $ ssh root@absys-demo
    root:~$ systemctl stop apache2.service
    root:~$ sudo --user postgres --login
    postgres:~$ dropdb absys
    postgres:~$ pg_restore --create --dbname=postgres /var/backups/pg_dump/absys_[ISO-DATE].dump
    postgres:~$ exit
    root:~$ systemctl start apache2.service
    root:~$ exit

Upgrade
=======

Zum Upgrade eines Demo Servers wie folgt vorgehen:

::

    $ scp -r wheelhouse root@absys-demo:/var/wheelhouse-archive/wheelhouse-$(date "+%Y-%m-%d")
    $ ssh root@absys-demo
    root:~$ rm /var/wheelhouse
    root:~$ ln -s /var/wheelhouse-archive/wheelhouse-$(date "+%Y-%m-%d") /var/wheelhouse
    root:~$ # Ggf. jetzt ein PostgreSQL Backup erstellen
    root:~$ su -l vagrant
    vagrant:~$ cd absys
    vagrant:absys$ git stash
    vagrant:absys$ git pull
    vagrant:absys$ git checkout <release_version>
    vagrant:absys$ git stash pop
    vagrant:absys$ ./setup/install.sh
    vagrant:absys$ git checkout master
    vagrant:absys$ exit
    root:~$ exit
