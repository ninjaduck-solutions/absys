# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0005_sozialamt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schliesstag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datum', models.DateField()),
                ('art', models.CharField(max_length=10, blank=True)),
                ('name', models.CharField(max_length=5, blank=True)),
                ('einrichtungen', models.ManyToManyField(related_name='schliesstage', verbose_name='Einrichtungen', to='stammdaten.Einrichtung')),
            ],
            options={
                'verbose_name': 'Schliesstag',
                'verbose_name_plural': 'Schliesstage',
            },
        ),
    ]
