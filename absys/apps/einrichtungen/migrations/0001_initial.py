# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Einrichtung',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(unique=True, verbose_name='Name', max_length=30)),
                ('kuerzel', models.CharField(unique=True, verbose_name='Kürzel', max_length=1)),
            ],
            options={
                'verbose_name': 'Einrichtung',
                'verbose_name_plural': 'Einrichtungen',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EinrichtungHatPflegesatz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('pflegesatz', models.DecimalField(decimal_places=2, max_digits=4)),
                ('pflegesatz_startdatum', models.DateField()),
                ('pflegesatz_enddatum', models.DateField()),
                ('pflegesatz_ferien', models.DecimalField(decimal_places=2, max_digits=4)),
                ('pflegesatz_ferien_startdatum', models.DateField()),
                ('pflegesatz_ferien_enddatum', models.DateField()),
                ('name', models.ForeignKey(related_name='pflegesaetze', to='einrichtungen.Einrichtung')),
            ],
            options={
                'verbose_name': 'Pflegesatz einer Einrichtung',
                'verbose_name_plural': 'Pflegesätze der Einrichtungen',
            },
        ),
        migrations.CreateModel(
            name='Ferien',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('startdatum', models.DateField()),
                ('enddatum', models.DateField()),
                ('einrichtungen', models.ManyToManyField(related_name='ferien', verbose_name='Einrichtungen', to='einrichtungen.Einrichtung')),
            ],
            options={
                'verbose_name': 'Ferien',
                'verbose_name_plural': 'Ferien',
            },
        ),
        migrations.CreateModel(
            name='Schliesstag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('datum', models.DateField()),
                ('art', models.CharField(max_length=50)),
                ('einrichtungen', models.ManyToManyField(related_name='schliesstage', verbose_name='Einrichtungen', to='einrichtungen.Einrichtung')),
            ],
            options={
                'verbose_name': 'Schliesstag',
                'verbose_name_plural': 'Schliesstage',
            },
        ),
        migrations.CreateModel(
            name='SchuelerInEinrichtung',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('eintritt', models.DateField()),
                ('austritt', models.DateField()),
                ('sozialamtbescheid_von', models.DateField()),
                ('sozialamtbescheid_bis', models.DateField()),
                ('pers_pflegesatz', models.DecimalField(default=0, decimal_places=2, max_digits=4)),
                ('pers_pflegesatz_startdatum', models.DateField(blank=True)),
                ('pers_pflegesatz_enddatum', models.DateField(blank=True)),
                ('pers_pflegesatz_ferien', models.DecimalField(default=0, decimal_places=2, max_digits=4)),
                ('pers_pflegesatz_ferien_startdatum', models.DateField(blank=True)),
                ('pers_pflegesatz_ferien_enddatum', models.DateField(blank=True)),
                ('einrichtung', models.ForeignKey(to='einrichtungen.Einrichtung')),
                ('schueler', models.ForeignKey(to='schueler.Schueler')),
            ],
            options={
                'verbose_name': 'Schueler in der Einrichtung',
                'verbose_name_plural': 'Schueler in den Einrichtungen',
                'ordering': ('schueler__nachname', 'schueler__vorname', '-austritt'),
            },
        ),
        migrations.AddField(
            model_name='einrichtung',
            name='schueler',
            field=models.ManyToManyField(related_name='einrichtungen', verbose_name='Schüler', to='schueler.Schueler', through='einrichtungen.SchuelerInEinrichtung'),
        ),
        migrations.AlterUniqueTogether(
            name='schuelerineinrichtung',
            unique_together=set([('schueler', 'einrichtung', 'eintritt', 'austritt')]),
        ),
    ]
