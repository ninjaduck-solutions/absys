# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 12:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0005_auto_20160817_1326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schueler',
            name='stufe',
        ),
        migrations.DeleteModel(
            name='Stufe',
        ),
    ]
