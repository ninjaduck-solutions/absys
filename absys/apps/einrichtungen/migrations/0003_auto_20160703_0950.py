# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0002_remove_schliesstag_einrichtungen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz',
            field=models.DecimalField(max_digits=4, decimal_places=2, default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_enddatum',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien',
            field=models.DecimalField(max_digits=4, decimal_places=2, default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien_enddatum',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien_startdatum',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_startdatum',
            field=models.DateField(null=True, blank=True),
        ),
    ]
