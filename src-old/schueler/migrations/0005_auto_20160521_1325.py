# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0004_remove_schueler_erstellungsdatum'),
    ]

    operations = [
        migrations.AddField(
            model_name='schueler',
            name='gruppe',
            field=models.ForeignKey(default=b'1', to='schueler.Gruppe'),
        ),
        migrations.AddField(
            model_name='schueler',
            name='stufe',
            field=models.ForeignKey(default=b'1', to='schueler.Stufe'),
        ),
    ]
