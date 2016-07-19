# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0009_auto_20160719_1923'),
        ('schueler', '0003_auto_20160719_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rechnung',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('startdatum', models.DateField(verbose_name='Startdatum')),
                ('enddatum', models.DateField(help_text='Das Enddatum muss nach dem Startdatum liegen.', verbose_name='Enddatum')),
                ('name_schueler', models.CharField(max_length=61, verbose_name='Name des Schülers')),
                ('summe', models.DecimalField(decimal_places=2, max_digits=7, null=True, verbose_name='Gesamtbetrag')),
                ('fehltage', models.PositiveIntegerField(default=0, verbose_name='Fehltage im Abrechnungszeitraum')),
                ('fehltage_jahr', models.PositiveIntegerField(default=0, verbose_name='Fehltage seit Eintritt in die Einrichtung')),
                ('fehltage_nicht_abgerechnet', models.PositiveIntegerField(default=0, verbose_name='Bisher nicht abgerechnete Fehltage')),
                ('max_fehltage', models.PositiveIntegerField(default=0, verbose_name='Maximale Fehltage zum Abrechnungstag')),
                ('schueler', models.ForeignKey(to='schueler.Schueler', verbose_name='Schüler')),
                ('sozialamt', models.ForeignKey(to='schueler.Sozialamt', verbose_name='Sozialamt')),
            ],
            options={
                'ordering': ('sozialamt', 'schueler', 'startdatum', 'enddatum'),
                'verbose_name_plural': 'Rechnungen',
                'verbose_name': 'Rechnung',
            },
        ),
        migrations.CreateModel(
            name='RechnungsPosition',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('datum', models.DateField(verbose_name='Datum')),
                ('name_einrichtung', models.CharField(max_length=20, verbose_name='Einrichtung')),
                ('tag_art', models.CharField(default='schule', max_length=20, choices=[('ferien', 'Ferientag'), ('schule', 'Schultag')], verbose_name='Schul- oder Ferientag')),
                ('abwesend', models.BooleanField(default=False, verbose_name='Abwesenheit')),
                ('pflegesatz', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Pflegesatz')),
                ('einrichtung', models.ForeignKey(to='einrichtungen.Einrichtung', verbose_name='Schüler')),
                ('rechnung', models.ForeignKey(null=True, related_name='positionen', to='abrechnung.Rechnung', verbose_name='Rechnung')),
                ('schueler', models.ForeignKey(to='schueler.Schueler', verbose_name='Schüler')),
                ('sozialamt', models.ForeignKey(to='schueler.Sozialamt', verbose_name='Sozialamt')),
            ],
            options={
                'ordering': ('sozialamt', 'schueler', 'einrichtung', 'datum'),
                'verbose_name_plural': 'Rechnungspositionen',
                'verbose_name': 'Rechnungsposition',
            },
        ),
        migrations.AlterUniqueTogether(
            name='rechnungsposition',
            unique_together=set([('schueler', 'datum')]),
        ),
        migrations.AlterUniqueTogether(
            name='rechnung',
            unique_together=set([('sozialamt', 'schueler', 'startdatum', 'enddatum')]),
        ),
    ]
