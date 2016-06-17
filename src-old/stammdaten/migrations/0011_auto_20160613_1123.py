# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0010_auto_20160613_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schueler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nachname', models.CharField(max_length=10)),
                ('vorname', models.CharField(max_length=10)),
                ('geburtsdatum', models.DateField()),
                ('bemerkungen', models.TextField(max_length=100)),
                ('buchungsnummer', models.CharField(max_length=13, blank=True)),
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
                ('pers_pflegesatz', models.DecimalField(default=0, max_digits=4, decimal_places=2)),
                ('pers_pflegesatz_startdatum', models.DateField()),
                ('pers_pflegesatz_enddatum', models.DateField()),
                ('pers_pflegesatz_ferien', models.DecimalField(default=0, max_digits=4, decimal_places=2)),
                ('pers_pflegesatz_ferien_startdatum', models.DateField()),
                ('pers_pflegesatz_ferien_enddatum', models.DateField()),
                ('einrichtung', models.ForeignKey(to='stammdaten.Einrichtung')),
                ('schueler', models.ForeignKey(to='stammdaten.Schueler')),
            ],
            options={
                'ordering': ('schueler__nachname', 'schueler__vorname', '-austritt'),
                'verbose_name': 'Schueler in der Einrichtung',
                'verbose_name_plural': 'Schueler in den Einrichtungen',
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
