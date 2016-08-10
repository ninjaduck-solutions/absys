# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0007_auto_20160707_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='einrichtunghatpflegesatz',
            name='pflegesatz_ferien_enddatum',
        ),
        migrations.RemoveField(
            model_name='einrichtunghatpflegesatz',
            name='pflegesatz_ferien_startdatum',
        ),
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien_enddatum',
        ),
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien_startdatum',
        ),
    ]
