# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Einrichtung',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('einrichtungsname', models.CharField(default='', max_length=200)),
                ('einrichtungspflegesatz_schultag', models.DecimalField(max_digits=4, decimal_places=2)),
                ('einrichtungspflegesatz_schultag_startdatum', models.DateField()),
                ('einrichtungspflegesatz_schultag_enddatum', models.DateField()),
                ('einrichtungspflegesatz_ferientag', models.DecimalField(max_digits=4, decimal_places=2)),
                ('einrichtungspflegesatz_ferientag_startdatum', models.DateField()),
                ('einrichtungspflegesatz_ferientag_enddatum', models.DateField()),
                ('erstellungsdatum', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Einrichtungen',
            },
        ),
        migrations.CreateModel(
            name='Ferientag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ferienname', models.CharField(max_length=30, blank=True)),
                ('startdatum', models.DateField()),
                ('enddatum', models.DateField()),
                ('erstellungsdatum', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Ferientage',
            },
        ),
        migrations.CreateModel(
            name='Gruppe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gruppenname', models.CharField(default='', max_length=400)),
                ('bemerkungen', models.CharField(max_length=200)),
                ('erstellungsdatum', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Gruppen',
            },
        ),
        migrations.CreateModel(
            name='Schliesstag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datum', models.DateField()),
                ('art', models.CharField(max_length=30, blank=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('erstellungsdatum', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Schliesstage',
            },
        ),
        migrations.CreateModel(
            name='Schueler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nachname', models.CharField(max_length=200)),
                ('vorname', models.CharField(max_length=200)),
                ('geburtsdatum', models.DateField()),
                ('bemerkungen', models.TextField(max_length=10000)),
                ('pers_pflegesatz', models.DecimalField(max_digits=4, decimal_places=2, blank=True)),
                ('buchungsnummer', models.CharField(default='', max_length=30, blank=True)),
                ('erstellungsdatum', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Schueler',
            },
        ),
        migrations.CreateModel(
            name='SchuelerInEinrichtung',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('erstellungsdatum', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('buchungsnummer', models.ForeignKey(related_name='+', default='', to='stammdaten.Schueler')),
                ('einrichtungsname', models.ForeignKey(related_name='+', default='', to='stammdaten.Einrichtung')),
                ('nachname', models.ForeignKey(related_name='+', default='', to='stammdaten.Schueler')),
                ('vorname', models.ForeignKey(related_name='+', default='', to='stammdaten.Schueler')),
            ],
            options={
                'verbose_name': 'Schueler in der Einrichtung',
                'verbose_name_plural': 'Schueler in der Einrichtung',
            },
        ),
        migrations.CreateModel(
            name='Sozialamt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sozialamtname', models.CharField(default='', max_length=200)),
                ('sozialamt_anschrift', models.CharField(max_length=400)),
                ('sozialamt_konto_iban', models.CharField(max_length=22)),
                ('sozialamt_konto_institut', models.CharField(max_length=400)),
                ('erstellungsdatum', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Sozialaemter',
            },
        ),
        migrations.CreateModel(
            name='Stufe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stufenname', models.CharField(default='', max_length=400)),
                ('bemerkungen', models.CharField(max_length=200)),
                ('erstellungsdatum', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Stufen',
            },
        ),
        migrations.AddField(
            model_name='schueler',
            name='stufe',
            field=models.ForeignKey(default='', to='stammdaten.Stufe'),
        ),
    ]
