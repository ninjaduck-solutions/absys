*****************
Demo Server Setup
*****************

Setup
=====

Zum Setup eines Demo Servers wie folgt vorgehen:

::

    $ scp dist/absys-*.whl root@absys-demo:/root
    $ ssh root@absys-demo
    root:~$ locale-gen en_US.UTF-8
    root:~$ wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
    root:~$ echo "deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main" > /etc/apt/sources.list.d/saltstack.list
    root:~$ apt-get update
    root:~$ apt-get --yes install git salt-minion
    root:~$ adduser --disabled-password --gecos "" vagrant
    root:~$ echo "vagrant ALL = NOPASSWD: ALL" >> /etc/sudoers
    root:~$ cp --verbose absys-*.whl /home/vagrant
    root:~$ su -l vagrant
    vagrant:~$ git clone ssh://git@h2516835.stratoserver.net:2050/srv/git/absys.git
    vagrant:~$ cd absys
    vagrant:absys-deployment$ sudo salt-call --local --file-root=salt/roots/salt --pillar-root=salt/roots/pillar state.apply
    vagrant:absys-deployment$ sudo salt-call --local --file-root=salt/roots/salt --pillar-root=salt/roots/pillar state.sls apache
    vagrant:absys-deployment$ sed -i 's/PACKAGE_PATH=.*/PACKAGE_PATH=\/home\/vagrant/' setup/install.sh
    vagrant:absys-deployment$ ./setup/install.sh
    vagrant:absys-deployment$ exit
    root:~$ exit

Upgrade
=======

Zum Upgrade eines Demo Servers wie folgt vorgehen:

::

    $ scp dist/absys-*.whl root@absys-demo:/root
    $ ssh root@absys-demo
    root:~$ cp --verbose absys-*.whl /home/vagrant
    root:~$ su -l vagrant
    vagrant:~$ cd absys
    vagrant:~$ git pull
    vagrant:absys-deployment$ ./setup/install.sh
    vagrant:absys-deployment$ exit
    root:~$ exit
