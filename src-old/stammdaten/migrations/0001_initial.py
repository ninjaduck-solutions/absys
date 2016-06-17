# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gruppe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', max_length=5)),
                ('bemerkungen', models.CharField(max_length=200)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Gruppe',
                'verbose_name_plural': 'Gruppen',
            },
        ),
    ]
