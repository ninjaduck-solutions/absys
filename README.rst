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

Die benötigte Software wird via `SaltStack
<https://docs.saltstack.com/en/latest/>`_ innerhalb der Vagrant Box
installiert.

Einrichten der Entwicklungsumgebung
===================================

Folgende Befehle ausführen, um die Vagrant Box als Entwicklungsumgebung einzurichten:

::

    > git clone ssh://git@h2516835.stratoserver.net:2050/srv/git/absys.git
    > cd absys
    > git checkout develop
    > vagrant up

Nutzer von Linux und OS X können sich direkt mit folgendem Befehl mit der Vagrant Box verbinden:

::

    > vagrant ssh

Windows Nutzer müssen sich mit PuTTY mit der Vagrant Box verbinden. Dazu sind
die folgenden Schritte zur Einrichtung der Verbindung nötig:

1. PuTTYgen öffnen
2. Conversions -> "Import key" anklicken
3. Den privaten SSH Key in ``absys/.vagrant/machines/default/virtualbox/private_key`` auswählen
4. "Save private key" anklicken, bei der folgenden Frage mit "Ja" antworten und den neuen Private Key im PPK Format speichern
5. PuTTY öffnen
6. Eine neue PuTTY Verbindung einrichten und wie folgt konfigurieren

     a) ``127.0.0.1`` als "Host Name" eintragen
     b) ``2222`` als Port eintragen
     c) In "Connection -> Data" ``vagrant`` in "Auto-login username" eintragen
     d) In "Connection -> SSH -> Auth" bei "Private key file for authentication" auf "Browse" klicken und die mit PuTTYgen ereugte PPK Datei asuwählen
     e) In "Session" im leeren Feld unter "Saved Sessions" einen Namen vergeben und auf "Save" klicken
     f) Gespeicherten Sessionnamen doppelt anklicken

.. note::

    Die in der Vagrant Box installierte Software und ihre Konfiguration sollen
    nur durch die Salt States verwaltet werden. Daher sollen alle Änderungen in
    den Verzeichnissen ``/salt/roots/salt`` (Software) und
    ``salt/roots/pillar`` (Konfiguration) vorgenommen werden.

Nach dem Login in die Vagrant Box wird automatisch ein Python 3 Virtual
Environment ``pyvenv`` aktiviert. Du erkennst das daran, dass der Name des
Virtual Environment in Klammern vor dem Prompt steht.

Arbeiten mit der Entwicklungsumgebung
=====================================

Um am Django Projekt zu arbeiten müssen die folgenden Befehle ausgeführt werden:

::

    $ cd /vagrant  # Wechselt ins Projektverzeichnis; nach jeder Anmeldung auszuführen
    $ make develop  # Installiert alle benötigten Pakete für das Projekt; nach jeder Veränderung an den verwendeten Django/Python Packages auszuführen
    $ make migrate  # Führt die Datenbank Migrationen aus; nach jeder Änderung an der Datenbank und beim initialen Erstellen nach 'make develop' auszuführen
    $ make runserver  #  Startet den Development-Webserver; vor jedem Versuch, die Website im Browser zu testen  auszuführen

.. note::

    Sollte das Virtual Environment (``pyvenv``) einmal kaputt gehen, folgende Schritte ausführen:

    ::

        $ cd  # Wechselt in das Home Verzeichnis
        $ rm -fr pyvenv
        $ exit
        > vagrant provision
        > vagrant ssh
        $ cd /vagrant
        $ make develop

Tipps
=====

- Du kannst `Zeal <https://zealdocs.org/>`_ auf deinem Host Betriebssystem installieren, um die Dokumentation aller im Projekt benutzten Softwarekomponenten offline verfügbar zu haben

::

    $ git flow init -d

    $ git flow feature start new-feature
