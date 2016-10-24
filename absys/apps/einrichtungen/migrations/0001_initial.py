# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 10:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schueler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Einrichtung',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name')),
                ('kuerzel', models.CharField(max_length=3, unique=True, verbose_name='Kürzel')),
                ('titel', models.IntegerField(help_text='Darf maximal fünf Ziffern haben.', unique=True, verbose_name='Titel')),
            ],
            options={
                'verbose_name': 'Einrichtung',
                'ordering': ['name'],
                'verbose_name_plural': 'Einrichtungen',
            },
        ),
        migrations.CreateModel(
            name='EinrichtungHatPflegesatz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('pflegesatz', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pflegesatz_ferien', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pflegesatz_startdatum', models.DateField()),
                ('pflegesatz_enddatum', models.DateField()),
                ('einrichtung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pflegesaetze', to='einrichtungen.Einrichtung')),
            ],
            options={
                'verbose_name': 'Pflegesatz einer Einrichtung',
                'verbose_name_plural': 'Pflegesätze der Einrichtungen',
            },
        ),
        migrations.CreateModel(
            name='Ferien',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('startdatum', models.DateField()),
                ('enddatum', models.DateField()),
                ('einrichtungen', models.ManyToManyField(related_name='ferien', to='einrichtungen.Einrichtung', verbose_name='Einrichtungen')),
            ],
            options={
                'verbose_name': 'Ferien',
                'verbose_name_plural': 'Ferien',
            },
        ),
        migrations.CreateModel(
            name='Schliesstag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('datum', models.DateField(unique=True)),
                ('art', models.CharField(max_length=50)),
                ('einrichtungen', models.ManyToManyField(related_name='schliesstage', to='einrichtungen.Einrichtung', verbose_name='Einrichtungen')),
            ],
            options={
                'verbose_name': 'Schließ\xadtag',
                'verbose_name_plural': 'Schließ\xadtage',
            },
        ),
        migrations.CreateModel(
            name='SchuelerInEinrichtung',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('eintritt', models.DateField(verbose_name='Eintritt')),
                ('austritt', models.DateField(help_text='Der Austritt muss nach dem Eintritt erfolgen.', verbose_name='Austritt')),
                ('pers_pflegesatz', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('pers_pflegesatz_ferien', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('pers_pflegesatz_startdatum', models.DateField(blank=True, null=True)),
                ('pers_pflegesatz_enddatum', models.DateField(blank=True, null=True)),
                ('fehltage_erlaubt', models.PositiveIntegerField(default=45)),
                ('einrichtung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anmeldungen', to='einrichtungen.Einrichtung')),
                ('schueler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='angemeldet_in_einrichtung', to='schueler.Schueler')),
                ('sozialamt', models.ForeignKey(help_text='<span style="font-size: 1.3em">Es wird automatisch das aktuelle Sozialamt des Schülers ausgewählt.<br><br>Soll der Schüler in dieser Einrichtung ein neues Sozialamt zugewiesen bekommen, muss wie folgt vorgegangen werden:<br><br>1. Das Austrittsdatum des aktuellen Datensatzes auf den letzten Tag für das alte Sozialamt setzen.<br>2. Das Sozialamt am Datensatz des Schülers ändern.<br>3. Den Schüler für den neuen Zeitraum der gleichen Einrichtung hinzufügen.<br><br></span>', on_delete=django.db.models.deletion.CASCADE, related_name='anmeldungen', to='schueler.Sozialamt')),
            ],
            options={
                'verbose_name_plural': 'Schüler in Einrichtungen',
                'ordering': ('schueler__nachname', 'schueler__vorname', '-austritt'),
                'verbose_name': 'Schüler in Einrichtung',
            },
        ),
        migrations.CreateModel(
            name='Standort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('anschrift', models.TextField()),
                ('konto_iban', models.CharField(max_length=22, verbose_name='IBAN')),
                ('konto_bic', models.CharField(max_length=12, verbose_name='BIC')),
                ('konto_institut', models.CharField(max_length=100, verbose_name='Institut')),
            ],
            options={
                'verbose_name': 'Standort',
                'verbose_name_plural': 'Standorte',
            },
        ),
        migrations.AddField(
            model_name='einrichtung',
            name='schueler',
            field=models.ManyToManyField(related_name='einrichtungen', through='einrichtungen.SchuelerInEinrichtung', to='schueler.Schueler', verbose_name='Schüler'),
        ),
        migrations.AddField(
            model_name='einrichtung',
            name='standort',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='einrichtungen', to='einrichtungen.Standort'),
        ),
        migrations.AlterUniqueTogether(
            name='schuelerineinrichtung',
            unique_together=set([('schueler', 'einrichtung', 'eintritt', 'austritt')]),
        ),
    ]
