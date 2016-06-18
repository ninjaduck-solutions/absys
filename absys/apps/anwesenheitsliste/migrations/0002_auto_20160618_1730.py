# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anwesenheitsliste', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='anwesenheit',
            unique_together=set([('schueler', 'einrichtungs_art', 'datum')]),
        ),
    ]
