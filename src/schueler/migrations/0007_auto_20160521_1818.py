# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0006_schueler_erstellungsdatum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schueler',
            name='erstellungsdatum',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
