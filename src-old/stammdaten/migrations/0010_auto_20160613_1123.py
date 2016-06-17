# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0009_auto_20160613_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schueler',
            name='einrichtungen',
        ),
        migrations.RemoveField(
            model_name='schueler',
            name='gruppe',
        ),
        migrations.RemoveField(
            model_name='schueler',
            name='sozialamt',
        ),
        migrations.RemoveField(
            model_name='schueler',
            name='stufe',
        ),
        migrations.AlterUniqueTogether(
            name='schuelerineinrichtung',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='einrichtung',
        ),
        migrations.RemoveField(
            model_name='schuelerineinrichtung',
            name='schueler',
        ),
        migrations.DeleteModel(
            name='Schueler',
        ),
        migrations.DeleteModel(
            name='SchuelerInEinrichtung',
        ),
    ]
