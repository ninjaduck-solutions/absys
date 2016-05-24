# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0005_auto_20160522_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schuelerineinrichtung',
            old_name='einrichtungsname',
            new_name='einrichtung',
        ),
        migrations.RenameField(
            model_name='schuelerineinrichtung',
            old_name='nachname',
            new_name='schueler',
        ),
    ]
