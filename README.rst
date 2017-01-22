******************
Abrechnungs-System
******************

Abrechnungssystem der SLSH und LZB.

Urheberrecht und Lizenz
=======================

Das Urheberrecht für den hier vorliegenden Programmcode liegt bei den Firmen
`IMTB <http://www.imtb.de/>`_ und `transcode <http://www.transcode.de/>`_
(2016-2017). Dieses Paket (sein Quellcode sowie möglicherweise kompilierte
Binärpakete) sind lizensiert unter der EUPL V.1.1. Der vollständige Lizenztext
liegt in der Datei ``LICENSE`` vor.

Voraussetzungen
===============

Zum Erstellen einer Entwicklungsumgebung muss die folgende Software installiert sein:

- Git
- `Vagrant 1.8 <https://www.vagrantup.com/>`_
- `VirtualBox 5.0 <https://www.virtualbox.org/>`_

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

.. note::

    Sollte beim Starten der Vagrant Box das Port Forwarding automatisch von
    Vagrant angepasst worden sein, werden nicht mehr die Ports verwendet, die
    hier genannt werden. Die neue Port Forwarding Konfiguration können mit
    folgendem Kommando ausgegeben werden:

    ::

        > vagrant port
        The forwarded ports for the machine are listed below. Please note that
        these values may differ from values configured in the Vagrantfile if the
        provider supports automatic port collision detection and resolution.

            22 (guest) => 2222 (host)
         61208 (guest) => 61208 (host)
          8000 (guest) => 8000 (host)

    Das Beispiel zeigt die Standardkonfiguration. Hier sind die Ports wie folgt
    konfiguriert:

    ==================== ================== ===========
    Dienst               Port (Vagrant Box) Port (Host)
    ==================== ================== ===========
    SSH/PuTTY            ``22``             ``2222``
    Glances (Monitoring) ``61208``          ``61208``
    Django (Webserver)   ``8000``           ``8000``
    ==================== ================== ===========

    Wenn Vagrant das Port Forwarding anpasst, kann die Ausgabe wie folgt
    aussehen:

    ::

        > vagrant port
        The forwarded ports for the machine are listed below. Please note that
        these values may differ from values configured in the Vagrantfile if the
        provider supports automatic port collision detection and resolution.

            22 (guest) => 2202 (host)
         61208 (guest) => 2201 (host)
          8000 (guest) => 2200 (host)

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

Weiterhin wird beim ersten Verbinden nach deinem Benutzernamen und deiner Mailadresse für git gefragt. Bitte eintragen.

Arbeiten mit der Entwicklungsumgebung
=====================================

Um am Django Projekt zu arbeiten müssen die folgenden Befehle ausgeführt werden:

::

    (pyvenv) vagrant@absys-dev:~$ cd /vagrant  # Wechselt ins Projektverzeichnis; nach jeder Anmeldung auszuführen
    (pyvenv) vagrant@absys-dev:/vagrant$ make develop  # Installiert alle benötigten Pakete für das Projekt; nach jeder Veränderung an den verwendeten Django/Python Packages auszuführen
    (pyvenv) vagrant@absys-dev:/vagrant$ make migrate  # Führt die Datenbank Migrationen aus; nach jeder Änderung an der Datenbank und beim initialen Erstellen nach 'make develop' auszuführen
    (pyvenv) vagrant@absys-dev:/vagrant$ make createsuperuser  # Einen neuen Django Superuser erstellen
    (pyvenv) vagrant@absys-dev:/vagrant$ make runserver  #  Startet den Development-Webserver; vor jedem Versuch, die Website im Browser zu testen  auszuführen

Das Django Projekt kann nun unter http://127.0.0.1:8000 im Browser aufgerufen werden.

.. note::

	Wenn das Hostsystem MS Windows ist, werden Zeilenumbrüche anders kodiert. Deswegen kann es sein, dass ``git status`` alle Dateien, die getracked werden als ``modified`` erkennt. In diesem Fall BEVOR eigener Code produziert wird

	::

		(pyvenv) vagrant@absys-dev:/vagrant$ git reset --hard

	ausführen. Dies setzt die Änderungen zurück und ``git status`` sollte keine Dateien mehr als ``modified`` anzeigen.

.. note::

    Sollen Zeilenenden auf Windowssystemen (CRLF) immer durch LF (Unix) ersetzt werden, lege eine Datei Namens ``.gitattributes``
    im Root-Verzeichnis des Projektes an und füge folgende Zeile in die Datei ein:

    ::

        *    text



.. note::

    Um alle Befehle zu sehen, die mit ``make`` ausgeführt werden können,
    einfach ``make`` ohne weitere Argumente aufrufen:

    ::

        (pyvenv) vagrant@absys-dev:/vagrant$ make

    Für alle Django Management Commands, die nicht von ``make`` erfasst werden,
    bitte folgendes Kommando benutzen:

    ::

        (pyvenv) vagrant@absys-dev:/vagrant$ envdir envs/dev/ python manage.py <DJANGO_COMMAND>

.. note::

    Sollte das Virtual Environment (``pyvenv``) einmal kaputt gehen, folgende Schritte ausführen:

    ::

        (pyvenv) vagrant@absys-dev:/vagrant$ cd  # Wechselt in das Home Verzeichnis
        (pyvenv) vagrant@absys-dev:~$ rm -fr pyvenv
        (pyvenv) vagrant@absys-dev:~$ exit
        > vagrant provision
        > vagrant ssh
        (pyvenv) vagrant@absys-dev:~$ cd /vagrant
        (pyvenv) vagrant@absys-dev:/vagrant$ make develop

.. note::

    Sollte die Vagrant Maschine einmal merkwürdiges Verhalten an den Tag legen, halte dich nicht lange mit der
    Fehlersuche auf. Committe und pushe deine letzten Änderungen am Code und führe anschließend in dem Terminal,
    in dem du erst ``vagrant up`` ausgeführt hast ``vagrant destroy`` und anschließend wieder ``vagrant up`` durch.

Arbeiten mit git-flow
=====================

We are using `git-flow <https://github.com/nvie/gitflow/>`_, a set of git
extensions for a branching model introduced by Vincent Driessen. You can read
more about it on `Vincent's blog
<http://nvie.com/posts/a-successful-git-branching-model/>`_, where you can also
find a `high-quality PDF illustrating the model
<http://nvie.com/files/Git-branching-model.pdf>`_. For your daily workflow
there also the `git-flow cheatsheet
<https://danielkummer.github.io/git-flow-cheatsheet/>`_ created by Daniel
Kummer, which is very helpful.

Dokumentation erstellen und öffnen
==================================

Die Dokumentation erklärt unter anderem das Erstellen eines Releases und
Deployment des Demo Servers.

Dokumentation erstellen:

::

    (pyvenv) vagrant@absys-dev:/vagrant$ make docs

Danch ist die Dokumentation unter ``docs/_build/html/index.html`` zu finden
(aus Sicht des Hosts).


Tipps
=====

.. note::

	Du kannst `Zeal <https://zealdocs.org/>`_ auf deinem Host Betriebssystem installieren, um die Dokumentation aller
	im Projekt benutzten Softwarekomponenten offline verfügbar zu machen.

.. note::

	Wenn du Programmcode vor der Implementation auf der Shell (IPython) ausprobierst, Fehler auftreten und du
	Dateien (und zwar nur Dateien! Keine Klassen- oder Funktionsimports) re-importieren möchtest, müssen
	folgende Kommandos ausgeführt werden:

	::

		>>> import imp
		>>> imp.reload(<Datei-/Modulname>)

.. note::

    Versucht man in einer frischen Umgebung nach dem Anlegen einiger Daten
    Rechnungen als PDF zu erzeugen scheitert ``wkhtmltopdf``. Dies passiert dann
    wenn auf dem System noch nicht ``envdir env/dev ./manage.py collectstatic``
    ausgeführt wurde da dann einige für die Generation relevante Assets noch
    nicht vorliegen. Beim Installieren auf Production oder Staging wird in der
    install.sh jedoch ``collectstatic`` aufgerufen, so dass dort dieser Problem
    nicht auftritt.

Setup-Paket erstellen
=====================

Das Setup-Paket wird für Installation/Upgrade der Staging- und Production-
Server benötigt.

Um die Deployment Vagrant Box zu benutzen, muss vorher das ``absys`` Paket
innnerhalb der dev Vagrant Box erstellt werden. Außerdem müssen alle Python
Wheels, die auf dem Server installiert werden sollen, erstellt und gesammelt
werden. Dazu wie folgt vorgehen:

::

    (pyvenv) vagrant@absys-dev:/vagrant$ make dist
    (pyvenv) vagrant@absys-dev:/vagrant$ make wheelhouse

.. note::

    Das ``absys`` Paket sollte am besten aus einem Release erstellt werden.
    Dieser kann mit ``git checkout 1.0.0`` wiederhergestellt werden, wobei
    "1.0.0" mit der gewünschten Version zu ersetzen ist. Nach dem Erstellen der
    Python Wheels wieder den Entwicklungsbranch mit ``git checkout develop``
    herstellen.

Danach die Deployment Vagrant Box erstellen. Um sicherzustellen, dass eine
saubere Umgebung vorliegt, wird die deployment Vagrant Box jedes mal komplett
neu erstellt. Dazu die folgenden Befehle in einem neuen Terminal ausführen:

::

    > vagrant destroy -f deployment
    > vagrant up deployment
    > vagrant ssh deployment
    vagrant@absys-deployment:~$ /vagrant/setup/install.sh

.. note::

    Hinweise zum Port Forwarding und zur Nutzung von ``vagrant ssh`` unter
    Windows finden sich weiter oben unter der Überschrift "Einrichten der
    Entwicklungsumgebung".

Nach der Installation testen, ob der Webserver unter https://127.0.0.1:8080
erreichbar ist. Da ein selbst-signiertes SSL Zertifikat benutzt wird, muss erst
eine Ausnahme für dieses hinzugefügt werden.

Nun zum Extrahieren der Konfiguration in der deployment Vagrant Box folgenden
Befehl ausführen:

::

    vagrant@absys-deployment:~$ /vagrant/bin/extract.sh

Alle folgenden Befehle müssen auf der dev Vagrant Box ausgeführt werden, da nur
dort ``git`` installiert ist. Da beide Vagrant Boxen das gleiche Verzeichnis
als Netzlaufwerk haben, ist das ohne Probleme möglich.

Das Verzeichnis ``setup`` auf Änderungen prüfen und ggf. einen Commit machen:

::

    (pyvenv) vagrant@absys-dev:/vagrant$ git status
    (pyvenv) vagrant@absys-dev:/vagrant$ git add setup
    (pyvenv) vagrant@absys-dev:/vagrant$ git commit

Das Skript ``extract.sh`` erstellt aus den Dateien im Verzeichnis ``setup`` und
dem kompletten Verzeichnis ``wheelhouse`` automatisch ein tar Archiv
``setup.tar.gz`` und legt dieses im Stammverzeichnis des Projekts ab. Dieses
Archiv kann an den Dienstleister übergeben werden. Es soll nicht Teil des Git
Repositories werden und wird daher bei Commits ignoriert.
