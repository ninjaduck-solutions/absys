# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0004_auto_20160609_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='april',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='august',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='dezember',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='februar',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='januar',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='juli',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='juni',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='maerz',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='mai',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='november',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='oktober',
        ),
        migrations.RemoveField(
            model_name='fehltageerlaubt',
            name='september',
        ),
        migrations.AddField(
            model_name='fehltageerlaubt',
            name='werte',
            field=models.CommaSeparatedIntegerField(default=3, max_length=35),
            preserve_default=False,
        ),
    ]
