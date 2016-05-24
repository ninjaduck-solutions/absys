# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schueler',
            name='gruppe',
        ),
        migrations.RemoveField(
            model_name='schueler',
            name='stufe',
        ),
    ]
