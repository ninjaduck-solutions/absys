# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0003_auto_20160703_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
