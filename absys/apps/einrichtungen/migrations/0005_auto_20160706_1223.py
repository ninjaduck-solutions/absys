# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0004_auto_20160703_1013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='einrichtunghatpflegesatz',
            old_name='name',
            new_name='einrichtung',
        ),
    ]
