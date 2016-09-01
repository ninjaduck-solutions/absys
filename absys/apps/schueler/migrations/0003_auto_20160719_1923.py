# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0002_auto_20160707_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fehltageschuelererlaubt',
            name='schueler',
        ),
        migrations.DeleteModel(
            name='FehltageSchuelerErlaubt',
        ),
    ]
