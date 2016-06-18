# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anwesenheitsliste', '0002_auto_20160618_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anwesenheit',
            name='schueler',
            field=models.ForeignKey(to='anwesenheitsliste.Schueler', related_name='anwesenheit', verbose_name='Schüler'),
        ),
    ]
