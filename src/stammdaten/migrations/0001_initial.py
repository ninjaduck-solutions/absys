# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Einrichtung',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('pflegesatz', models.DecimalField(max_digits=4, decimal_places=2)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Einrichtung',
                'verbose_name_plural': 'Einrichtungen',
            },
        ),
        migrations.CreateModel(
            name='Ferien',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('startdatum', models.DateField()),
                ('enddatum', models.DateField()),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
                ('einrichtungen', models.ManyToManyField(related_name='ferien', verbose_name='Einrichtungen', to='stammdaten.Einrichtung')),
            ],
            options={
                'verbose_name': 'Ferien',
                'verbose_name_plural': 'Ferien',
            },
        ),
        migrations.CreateModel(
            name='Gruppe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', max_length=400)),
                ('bemerkungen', models.CharField(max_length=200)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Gruppe',
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
                ('einrichtungen', models.ManyToManyField(related_name='schliesstage', verbose_name='Einrichtungen', to='stammdaten.Einrichtung')),
            ],
            options={
                'verbose_name': 'Schliesstag',
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
                ('pers_pflegesatz', models.DecimalField(default=0, max_digits=4, decimal_places=2)),
                ('buchungsnummer', models.CharField(max_length=30, blank=True)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Schueler',
                'verbose_name_plural': 'Schueler',
            },
        ),
        migrations.CreateModel(
            name='SchuelerInEinrichtung',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eintritt', models.DateField()),
                ('austritt', models.DateField()),
                ('sozialamtbescheid_von', models.DateField()),
                ('sozialamtbescheid_bis', models.DateField()),
                ('einrichtung', models.ForeignKey(to='stammdaten.Einrichtung')),
                ('schueler', models.ForeignKey(to='stammdaten.Schueler')),
            ],
            options={
                'verbose_name': 'Schueler in der Einrichtung',
                'verbose_name_plural': 'Schueler in den Einrichtungen',
            },
        ),
        migrations.CreateModel(
            name='Sozialamt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', max_length=200)),
                ('anschrift', models.CharField(max_length=400)),
                ('konto_iban', models.CharField(max_length=22)),
                ('konto_institut', models.CharField(max_length=400)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Sozialamt',
                'verbose_name_plural': 'Sozialaemter',
            },
        ),
        migrations.CreateModel(
            name='Stufe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', max_length=400)),
                ('bemerkungen', models.CharField(max_length=200)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Stufe',
                'verbose_name_plural': 'Stufen',
            },
        ),
        migrations.AddField(
            model_name='schueler',
            name='einrichtungen',
            field=models.ManyToManyField(to='stammdaten.Einrichtung', through='stammdaten.SchuelerInEinrichtung'),
        ),
        migrations.AddField(
            model_name='schueler',
            name='gruppe',
            field=models.ForeignKey(to='stammdaten.Gruppe'),
        ),
        migrations.AddField(
            model_name='schueler',
            name='sozialamt',
            field=models.ForeignKey(to='stammdaten.Sozialamt'),
        ),
        migrations.AddField(
            model_name='schueler',
            name='stufe',
            field=models.ForeignKey(to='stammdaten.Stufe'),
        ),
        migrations.AlterUniqueTogether(
            name='schuelerineinrichtung',
            unique_together=set([('schueler', 'einrichtung', 'eintritt', 'austritt')]),
        ),
    ]
