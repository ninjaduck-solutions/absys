# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0002_stufe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Einrichtung',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
                ('kuerzel', models.CharField(max_length=1)),
                ('pflegesatz', models.DecimalField(max_digits=4, decimal_places=2)),
                ('pflegesatz_startdatum', models.DateField()),
                ('pflegesatz_enddatum', models.DateField()),
                ('pflegesatz_ferien', models.DecimalField(max_digits=4, decimal_places=2)),
                ('pflegesatz_ferien_startdatum', models.DateField()),
                ('pflegesatz_ferien_enddatum', models.DateField()),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Einrichtung',
                'verbose_name_plural': 'Einrichtungen',
            },
        ),
    ]
