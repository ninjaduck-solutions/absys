# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0010_einrichtung_pers_bkz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='einrichtung',
            name='pers_bkz',
            field=models.BooleanField(default=False, verbose_name='Einrichtung mit persönlichen BKZ?'),
        ),
    ]
