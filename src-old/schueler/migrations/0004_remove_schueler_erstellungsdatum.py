# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0003_auto_20160521_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schueler',
            name='erstellungsdatum',
        ),
    ]
