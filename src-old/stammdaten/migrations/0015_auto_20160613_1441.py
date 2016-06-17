# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0014_auto_20160613_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_enddatum',
            field=models.DateField(default='2016-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien_enddatum',
            field=models.DateField(default='2016-12-31'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien_startdatum',
            field=models.DateField(default='2016-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_startdatum',
            field=models.DateField(default='2016-12-31'),
            preserve_default=False,
        ),
    ]
