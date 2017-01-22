******************
Installation AbSys
******************

Folgende Schritte sind zur Installation von AbSys Staging- und Production-
Servern nötig:

1. Alle in der Datei ``packages.txt`` enthaltenen Ubuntu-Pakete installieren:

    $ sudo apt-get install $(cat packages.txt)

2. Die folgenden Dateien in die entsprechenden Pfade kopieren:

    - ``000-default.conf`` (Beispiel: ``/etc/apache2/sites-available/000-default.conf``)
    - ``pg_hba.conf`` (Beispiel: ``/etc/postgresql/9.5/main/pg_hba.conf``)
    - ``wsgi.conf`` (Beispiel: ``/etc/apache2/conf-available/wsgi.conf``)

3. Jede der im vorherigen Schritt genannten Datei enthält Kommentare, die
   erklären, ob gegebenenfalls Anpassungen vorgenommen werden müssen und wie
   diese durchzuführen sind. Insbesondere ist es wichtig, ein Python Virtual
   Environment zu erstellen, in das alle Python Pakete später installiert
   werden können. Die Erstellung des Python Virtual Environments wird in der
   Datei ``000-default.conf`` beschrieben.

4. Die Apache Site ``000-default.conf`` muss aktiviert werden:

    $ sudo a2ensite 000-default

6. Die Apache Konfiguration ``wsgi.conf`` muss aktiviert werden:

    $ sudo a2enconf wsgi

7. Die in ``install.sh`` definierte Variable ``PACKAGE_PATH`` muss den Pfad zum
   Verzeichnis ``wheelhouse`` enthalten. Dieses Verzeichnis enthält alle zur
   Installation benötigten Python Pakete als Wheels.

8. Konfiguration in ``install.sh`` anpassen, dann Skript starten. Das Python
   Virtual Environment wird automatisch aktiviert.

9. Fertig! :-)

Urheberrecht und Lizenz
=======================

Das Urheberrecht für den hier vorliegenden Programmcode liegt bei den Firmen
`IMTB <http://www.imtb.de/>`_ und `transcode <http://www.transcode.de/>`_
(2016-2017). Dieses Paket (sein Quellcode sowie möglicherweise kompilierte
Binärpakete) sind lizensiert unter der EUPL V.1.1. Der vollständige Lizenztext
liegt in der Datei ``LICENSE`` vor.
