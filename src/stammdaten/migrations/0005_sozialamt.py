# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0004_ferien'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sozialamt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', max_length=10)),
                ('anschrift', models.CharField(max_length=20)),
                ('konto_iban', models.CharField(max_length=22)),
                ('konto_institut', models.CharField(max_length=10)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Sozialamt',
                'verbose_name_plural': 'Sozialaemter',
            },
        ),
    ]
