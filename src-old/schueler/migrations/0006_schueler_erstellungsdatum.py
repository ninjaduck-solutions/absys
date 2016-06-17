# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0005_auto_20160521_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='schueler',
            name='erstellungsdatum',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 21, 18, 13, 24, 346875)),
        ),
    ]
