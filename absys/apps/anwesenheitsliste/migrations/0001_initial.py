# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anwesenheit',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('datum', models.DateField(verbose_name='Datum')),
                ('abwesend', models.BooleanField(verbose_name='Abwesend', default=False)),
            ],
            options={
                'verbose_name': 'Anwesenheit',
                'verbose_name_plural': 'Anwesenheiten',
                'ordering': ['datum', 'schueler'],
            },
        ),
        migrations.CreateModel(
            name='EinrichtungsArt',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30, verbose_name='Name', unique=True)),
                ('kuerzel', models.CharField(max_length=1, verbose_name='Kürzel', unique=True)),
            ],
            options={
                'verbose_name': 'Einrichtung',
                'verbose_name_plural': 'Einrichtungen',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Schueler',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('vorname', models.CharField(max_length=30, verbose_name='Vorname')),
                ('nachname', models.CharField(max_length=30, verbose_name='Nachname')),
                ('einrichtungs_art', models.ForeignKey(verbose_name='Einrichtung', to='anwesenheitsliste.EinrichtungsArt')),
            ],
            options={
                'verbose_name': 'Schüler',
                'verbose_name_plural': 'Schüler',
                'ordering': ['nachname', 'vorname'],
            },
        ),
        migrations.AddField(
            model_name='anwesenheit',
            name='einrichtungs_art',
            field=models.ForeignKey(verbose_name='Einrichtung', to='anwesenheitsliste.EinrichtungsArt'),
        ),
        migrations.AddField(
            model_name='anwesenheit',
            name='schueler',
            field=models.ForeignKey(verbose_name='Schüler', to='anwesenheitsliste.Schueler'),
        ),
    ]
