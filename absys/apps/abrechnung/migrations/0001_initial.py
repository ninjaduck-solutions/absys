# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0003_auto_20160719_1923'),
        ('einrichtungen', '0009_auto_20160719_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rechnung',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('startdatum', models.DateField(verbose_name='Startdatum')),
                ('enddatum', models.DateField(help_text='Das Enddatum muss nach dem Startdatum liegen.', verbose_name='Enddatum')),
                ('name_schueler', models.CharField(max_length=61, verbose_name='Name des Schülers')),
                ('summe', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Gesamtbetrag', null=True)),
                ('fehltage', models.PositiveIntegerField(default=0, verbose_name='Fehltage im Abrechnungszeitraum')),
                ('fehltage_gesamt', models.PositiveIntegerField(default=0, verbose_name='Fehltage seit Eintritt in die Einrichtung')),
                ('fehltage_nicht_abgerechnet', models.PositiveIntegerField(default=0, verbose_name='Bisher nicht abgerechnete Fehltage')),
                ('max_fehltage', models.PositiveIntegerField(default=0, verbose_name='Maximale Fehltage zum Abrechnungstag')),
                ('schueler', models.ForeignKey(related_name='rechnungen', to='schueler.Schueler', verbose_name='Schüler')),
                ('sozialamt', models.ForeignKey(related_name='rechnungen', to='schueler.Sozialamt', verbose_name='Sozialamt')),
            ],
            options={
                'verbose_name': 'Rechnung',
                'verbose_name_plural': 'Rechnungen',
                'ordering': ('sozialamt', 'schueler', 'startdatum', 'enddatum'),
            },
        ),
        migrations.CreateModel(
            name='RechnungsPosition',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('datum', models.DateField(verbose_name='Datum')),
                ('name_einrichtung', models.CharField(max_length=20, verbose_name='Einrichtung')),
                ('tag_art', models.CharField(max_length=20, verbose_name='Schul- oder Ferientag', choices=[('ferien', 'Ferientag'), ('schule', 'Schultag')], default='schule')),
                ('abwesend', models.BooleanField(default=False, verbose_name='Abwesenheit')),
                ('pflegesatz', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Pflegesatz')),
                ('einrichtung', models.ForeignKey(to='einrichtungen.Einrichtung', verbose_name='Schüler')),
                ('rechnung', models.ForeignKey(related_name='positionen', null=True, to='abrechnung.Rechnung', verbose_name='Rechnung')),
                ('schueler', models.ForeignKey(to='schueler.Schueler', verbose_name='Schüler')),
                ('sozialamt', models.ForeignKey(to='schueler.Sozialamt', verbose_name='Sozialamt')),
            ],
            options={
                'verbose_name': 'Rechnungsposition',
                'verbose_name_plural': 'Rechnungspositionen',
                'ordering': ('sozialamt', 'schueler', 'einrichtung', 'datum'),
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
