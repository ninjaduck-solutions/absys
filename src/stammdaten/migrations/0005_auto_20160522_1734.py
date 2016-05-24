# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0004_auto_20160522_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='buchungsnummer',
        ),
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='vorname',
        ),
        migrations.AlterField(
            model_name='schueler',
            name='buchungsnummer',
            field=models.CharField(default='', max_length=30, null=True, blank=True),
        ),
    ]
