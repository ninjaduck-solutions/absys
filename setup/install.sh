#!/usr/bin/env bash
# Installation und Konfiguration AbSys

set -o errexit
set -o nounset
set -o pipefail
set -o verbose

# PACKAGE_PATH Variable anpassen. Dies kann entweder ein vollständiger Pfad
# oder ein URL sein, an dem pip alle für die Installation nötigen Python Pakete
# finden kann.
PACKAGE_PATH=/vagrant/wheelhouse

# Pfad zum Python Virtual Environment, in das alle Python Pakete später
# installiert werden. Falls nötig anpassen.
VENV_PATH=${HOME}/pyvenv

# Hier, falls nötig, weitere Optionen für pip angeben. Beispiel:
# PIP_DEFAULT_OPTIONS="--proxy https://proxy.example.com"
# pip Dokumentation: https://pip.pypa.io/
PIP_DEFAULT_OPTIONS=""

# Erstellen der envdir Verzeichnisse
sudo mkdir -p /var/envdir/absys
sudo chgrp -R www-data /var/envdir
sudo chmod -R g=rX,o= /var/envdir

# Django Konfiguration, bitte wie benötigt anpassen.
#
# Python Pfad zum Modul, das die zu benutzenden Django Einstellungen enthält.
echo 'absys.config.settings.public' | sudo tee /var/envdir/absys/DJANGO_SETTINGS_MODULE

# Name der Klasse, die die zu benutzenden Django Einstellungen enthält.
# Mögliche Werte: Staging oder Production
echo 'Staging' | sudo tee /var/envdir/absys/DJANGO_CONFIGURATION

# Konfiguration der Datenbank-Verbindung, siehe pg_hba.conf.
# Schema: postgres://BENUTZER:PASSWORT@localhost/DATENBANKNAME
# PASSWORT UNBEDINGT ÄNDERN!
echo 'postgres://absys:absys@localhost/absys' | sudo tee /var/envdir/absys/DEFAULT_DATABASE_URL

# Dauer in Sekunden, die die Datenbankverbindung aufrecht gehalten wird.
echo '600' | sudo tee /var/envdir/absys/DEFAULT_CONN_MAX_AGE

# Geheimer Schlüssel, der für kryptografische Signaturen benutzt wird.
# UNBEDINGT ÄNDERN! - SOLLTE 50 BELIEBIGE ZEICHEN ENTHALTEN.
echo 'INSECURE' | sudo tee /var/envdir/absys/DJANGO_SECRET_KEY

# E-Mail Adresse, die als Absender für automatische E-Mails benutzt wird.
echo 'noreply@example.com' | sudo tee /var/envdir/absys/DJANGO_DEFAULT_FROM_EMAIL

# SMTP Host.
# echo 'localhost' | sudo tee /var/envdir/absys/DJANGO_EMAIL_HOST
# SMTP Passwort.
echo 'INSECURE' | sudo tee /var/envdir/absys/DJANGO_EMAIL_HOST_PASSWORD

# SMTP User.
echo 'noreply@example.com' | sudo tee /var/envdir/absys/DJANGO_EMAIL_HOST_USER

# SMTP Port.
# echo '465' | sudo tee /var/envdir/absys/DJANGO_EMAIL_PORT

# SSL für SMTP benutzen, Port 465.
# echo 'True' | sudo tee /var/envdir/absys/DJANGO_EMAIL_USE_SSL

# TLS für SMTP benutzen, Port 587.
# echo 'False' | sudo tee /var/envdir/absys/DJANGO_EMAIL_USE_TLS

# Pfad zum Verzeichnis für alle Uploads, alle Dateien sollten als Backup
# gesichert werden.
echo "${HOME}/media" | sudo tee /var/envdir/absys/DJANGO_MEDIA_ROOT

# Pfad zum Verzeichnis für statische Dateien, diese ändern sich bei jedem
# Deployment und müssen nicht zwingend als Backup gesichert werden.
echo "${HOME}/static_root" | sudo tee /var/envdir/absys/DJANGO_STATIC_ROOT

# Liste der Hostnamen und Domains, die diese Website ausliefern soll. Hier die
# IP Adresse und/oder den Domainnamen mit Kommata getrennt eintragen.
# Bei fehlerhafter Konfiguration ist "Bad Request (400)" im Browser zu sehen.
echo '127.0.0.1,localhost' | sudo tee /var/envdir/absys/DJANGO_ALLOWED_HOSTS

# Sessionlänge in Sekunden. Nach Ablauf wird der user "ausgeloggt".
# echo "7200" | sudo tee /var/envdir/absys/DJANGO_SESSION_COOKIE_AGE

# Liste von Administratoren, die über Fehler via E-Mail informiert werden.
# echo "'Ada Lovelace',ada@example.com;'Bea Blue',bea@example.com" | sudo tee /var/envdir/absys/DJANGO_ADMINS

# Anzahl der Tage, die im aktuellen Monat für rückwirkende Änderungen der
# Anwesenheitsliste im Frontend zur Verfügung stehen.
# echo '15' | sudo tee /var/envdir/absys/DJANGO_ABSYS_ANWESENHEIT_TAGE_VORMONAT_ERLAUBT

# Möglichkeit zur Deaktivierung der Prüfung des Datums in der
# Anwesenheitsliste im Frontend.
# echo 'True' | sudo tee /var/envdir/absys/DJANGO_ABSYS_ANWESENHEIT_DATUMSPRUEFUNG

# Anzahl der Tage bis zur Fälligkeit einer Rechnung einer Einrichtung
# echo '31' | sudo tee /var/envdir/absys/DJANGO_ABSYS_TAGE_FAELLIGKEIT_EINRICHTUNG_RECHNUNG

# Feste Adresse der Schule
# echo 'Musterschule\nMusterstr. 42\n23232 Musterstadt' | sudo tee /var/envdir/absys/DJANGO_ABSYS_ADRESSE_SCHULE

# Ob das Buchungskennzeichen des Sozialamtes der Sozialamtsrechnung für alle ihre
# Einrichtungsrechnungen verwendet werden soll.
# echo 'False' | sudo tee /var/envdir/absys/DJANGO_ABSYS_NUTZE_SOZIALAMTS_BUCHUNGSKENNZEICHEN


# Konfiguration der automatierten 'Hintergrundprüfungen'/Benachrichtigungen.
# Anzahl der Buchungskennzeichen die unterschritten werden muss um eine
# 'Buchungskennzeichen gehen aus' Benachrichtigung zu veranlassen.
# echo '30' | sudo tee /var/envdir/absys/DJANGO_ABSYS_BUCHUNGSKENNZEICHEN_MIN_VERBLEIBEND

# Anzahl der Tage die ein Schüler noch in einer Einrichtung verbleibend ist
# bevor eine Benachrichtigung ausgelöst wird.
# echo '30' | sudo tee /var/envdir/absys/DJANGO_ABSYS_EINRICHTUNG_MIN_VERBLEIBENDE_TAGE

# Anzahl der Tage für ``EinrichtungHatPflegesatz.pflegesatz_enddatum``
# die wenn unterschritten eine Bennachrichtigung auslöst.
# echo '30' | sudo tee /var/envdir/absys/DJANGO_ABSYS_EINRICHTUNG_HAT_PFLEGESATZ_MIN_VERBLEIBENDE_TAGE

# Anzahl der Tage für ``Bettengeldsatz.enddatum`` die wenn unterschritten
# eine Bennachrichtigung auslöst.
# echo '30' | sudo tee /var/envdir/absys/DJANGO_ABSYS_BETTENGELDSATZ_MIN_VERBLEIBENDE_TAGE

# SaxMBS Konfiguration
# SaxMBS Anord-Kz - "J" oder "N"
# echo 'J' | sudo tee /var/envdir/absys/DJANGO_ABSYS_SAX_ANORDKZ
# SaxMBS Ebene 1 - String, muss acht Stellen haben
# echo '        ' | sudo tee /var/envdir/absys/DJANGO_ABSYS_SAX_EBENE_1
# SaxMBS Kapitel - Integer, darf maximal fünf Stellen haben; OHNE FÜHRENDE NULLEN ANGEBEN!
# echo '12345' | sudo tee /var/envdir/absys/DJANGO_ABSYS_SAX_KAPITEL
# SaxMBS Mahnschlüssel - Integer, darf maximal zwei Stellen haben
# echo '10' | sudo tee /var/envdir/absys/DJANGO_ABSYS_SAX_MAHNSCHLUESSEL
# SaxMBS SEPA - Integer, muss eine Stelle haben
# echo '1' | sudo tee /var/envdir/absys/DJANGO_ABSYS_SAX_SEPA
# SaxMBS Währung - String, darf maximal drei Stellen haben
# echo 'EUR' | sudo tee /var/envdir/absys/DJANGO_ABSYS_SAX_WAEHRUNG
# SaxMBS Zahlungsanzeigeschlüssel - Integer, darf maximal zwei Stellen haben
# echo '10' | sudo tee /var/envdir/absys/DJANGO_ABSYS_SAX_ZAHLUNGSANZEIGESCHLUESSEL
# SaxMBS Zinsschlüssel - Integer, muss eine Stelle haben
# echo '1' | sudo tee /var/envdir/absys/DJANGO_ABSYS_SAX_ZINSSCHLUESSEL

# Lockdown-Schutz aktivieren/deaktivieren
# echo 'True' | sudo tee /var/envdir/absys/DJANGO_LOCKDOWN_ENABLED

# Passwort für den Lockdown-Schutz
# echo '1234' | sudo tee /var/envdir/absys/DJANGO_LOCKDOWN_PASSWORDS

# Berechtigungen korrigieren
sudo chgrp -R www-data /var/envdir/absys && sudo chmod -R g=rX,o= /var/envdir/absys

# Installation/Upgrade AbSys und den abhängigen Paketen. Es werden nur Pakete
# aus ${PACKAGE_PATH} installiert, es findet kein Download statt.
${VENV_PATH}/bin/python -m pip install ${PIP_DEFAULT_OPTIONS} --force-reinstall --ignore-installed --no-index --find-links ${PACKAGE_PATH} --upgrade absys

# Deployment Check, Datenbank Migration und Sammeln der statischen Dateien.
sudo ${VENV_PATH}/bin/envdir /var/envdir/absys ${VENV_PATH}/bin/manage.py check --deploy
sudo ${VENV_PATH}/bin/envdir /var/envdir/absys ${VENV_PATH}/bin/manage.py migrate
sudo ${VENV_PATH}/bin/envdir /var/envdir/absys ${VENV_PATH}/bin/manage.py collectstatic --noinput
sudo systemctl reload apache2.service

# Täglichen cron job für Benachrichtigungen anlegen
echo -e "#! /bin/sh\n${VENV_PATH}/bin/envdir /var/envdir/absys $VENV_PATH/bin/manage.py benachrichtige" | sudo tee /etc/cron.daily/absys_benachrichtigungen
sudo chmod +x /etc/cron.daily/absys_benachrichtigungen

set +o verbose

echo
echo "###############################################################################################"
echo
echo "Installation abgeschlossen"
echo
echo "Folgende Umgebungsvariablen werden JETZT in /var/envdir/absys zur Konfiguration benutzt:"
echo
sudo ls -1 /var/envdir/absys
echo
echo "Es wurde ein neuer täglicher cron job unter /etc/cron.daily/absys_benachrichtigungen hinzugefügt!"
echo
echo "Nach der initialen Installation folgenden Befehle ausführen, um die Daten für das"
echo "Website Model zu laden und einen neuen Superuser zu erstellen:"
echo
echo "sudo ${VENV_PATH}/bin/envdir /var/envdir/absys ${VENV_PATH}/bin/manage.py loaddata sites"
echo "sudo ${VENV_PATH}/bin/envdir /var/envdir/absys ${VENV_PATH}/bin/manage.py createsuperuser"
echo
echo "Danach kann man sich mit dem Superuser anmelden und weitere Benutzer erstellen."
echo "Außerdem sollte der Domainname der importierten Website im Admin (Verwaltung) angepasst werden."
echo
echo "###############################################################################################"
