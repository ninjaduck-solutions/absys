# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0003_auto_20160609_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='fehltageerlaubt',
            name='jahr',
            field=models.PositiveIntegerField(default=2016, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='april',
            field=models.PositiveIntegerField(default=15),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='august',
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='dezember',
            field=models.PositiveIntegerField(default=45),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='februar',
            field=models.PositiveIntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='januar',
            field=models.PositiveIntegerField(default=4),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='juli',
            field=models.PositiveIntegerField(default=26),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='juni',
            field=models.PositiveIntegerField(default=23),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='maerz',
            field=models.PositiveIntegerField(default=11),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='mai',
            field=models.PositiveIntegerField(default=19),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='november',
            field=models.PositiveIntegerField(default=41),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='oktober',
            field=models.PositiveIntegerField(default=38),
        ),
        migrations.AlterField(
            model_name='fehltageerlaubt',
            name='september',
            field=models.PositiveIntegerField(default=34),
        ),
    ]
