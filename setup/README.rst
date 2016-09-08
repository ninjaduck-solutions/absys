******************
Installation AbSys
******************

Folgende Schritte sind zur Installation von AbSys Staging- und Production-Servern nötig:

1. Die Dateien ``history.log`` und ``packages.txt`` enthalten alle Informationen zu den zu installierenden Ubuntu-Paketen.
2. Die folgenden Dateien in die entsprechenden Pfade kopieren:

    - ``django.conf`` (Beispiel: ``/etc/apache2/sites-available/django.conf``)
    - ``pg_hba.conf`` (Beispiel: ``/etc/postgresql/9.5/main/pg_hba.conf``)
    - ``wsgi.conf`` (Beispiel: ``/etc/apache2/conf-available/wsgi.conf``)

3. Jede Datei enthält Kommentare, die erklären, welche Anpassungen vorgenommen werden müssen.
4. Konfiguration in ``install.sh`` anpassen, dann Skript starten.
5. Fertig! :-)
