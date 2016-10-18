******************
Installation AbSys
******************

Folgende Schritte sind zur Installation von AbSys Staging- und Production-
Servern nötig:

1. Alle in der Datei ``packages.txt`` enthaltenen Ubuntu-Pakete installieren.
2. Die folgenden Dateien in die entsprechenden Pfade kopieren:

    - ``django.conf`` (Beispiel: ``/etc/apache2/sites-available/django.conf``)
    - ``pg_hba.conf`` (Beispiel: ``/etc/postgresql/9.5/main/pg_hba.conf``)
    - ``wsgi.conf`` (Beispiel: ``/etc/apache2/conf-available/wsgi.conf``)

3. Jede der im vorherigen Schritt genannten Datei enthält Kommentare, die
   erklären, ob gegebenenfalls Anpassungen vorgenommen werden müssen und wie
   diese durchzuführen sind. Insbesondere ist es wichtig, ein Python Virtual
   Environment zu erstellen, in das alle Python Pakete später installiert
   werden können. Die Erstellung des Python Virtual Environments wird in der
   Datei ``django.conf`` beschrieben.
4. Die neue Apache Site in ``django.conf`` muss aktiviert werden.
5. Das AbSys Python Paket (``absys-*.whl``) in den in ``install.sh`` in der
   Variable ``PACKAGE_PATH`` definierten Pfad kopieren. Falls nötig den in
   ``PACKAGE_PATH`` definierten Pfad ändern.
6. Das vorher erstellte Python Virtual Environment aktivieren.
7. Konfiguration in ``install.sh`` anpassen, dann Skript starten mit
   aktiviertem Python Virtual Environment starten.
8. Fertig! :-)
