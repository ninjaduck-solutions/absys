# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0013_auto_20160613_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_enddatum',
        ),
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien_enddatum',
        ),
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien_startdatum',
        ),
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_startdatum',
        ),
    ]
