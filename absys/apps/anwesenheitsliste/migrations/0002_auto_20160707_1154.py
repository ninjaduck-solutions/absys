# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anwesenheitsliste', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anwesenheit',
            name='datum',
            field=models.DateField(verbose_name='Datum', db_index=True),
        ),
    ]
