# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0003_einrichtung'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ferien',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
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
    ]
