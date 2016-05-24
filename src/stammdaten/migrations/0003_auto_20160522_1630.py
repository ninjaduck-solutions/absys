# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0002_auto_20160522_1612'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ferientag',
            new_name='Ferien',
        ),
        migrations.AlterModelOptions(
            name='ferien',
            options={'managed': True, 'verbose_name_plural': 'Ferien'},
        ),
    ]
