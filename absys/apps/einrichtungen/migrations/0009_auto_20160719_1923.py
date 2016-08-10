# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0008_auto_20160707_1900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='sozialamtbescheid_bis',
        ),
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='sozialamtbescheid_von',
        ),
        migrations.AddField(
            model_name='schuelerineinrichtung',
            name='fehltage_erlaubt',
            field=models.PositiveIntegerField(default=45),
        ),
    ]
