******************
Abrechnungs-System
******************

Abrechnungssystem der SLSH und LZH.

Voraussetzungen
===============

Zum Erstellen einer Entwicklungsumgebung muss die folgende Software installiert sein:

- Git
- `Vagrant <https://www.vagrantup.com/>`_
- `VirtualBox <https://www.virtualbox.org/>`_

Einrichten der Entwicklungsumgebung
===================================

Folgende Befehle ausführen, um die Entwicklungsumgebung einzurichten:

::

    $ git clone ssh://git@h2516835.stratoserver.net:2050/srv/git/absys.git
    $ cd absys
    $ git checkout develop
    $ vagrant up

    $ git flow init -d

    $ git flow feature start new-feature

Detailed installation instructions for this Djangp project can be found in
``docs/installation.rst``.
