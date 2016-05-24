# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0003_auto_20160522_1630'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='einrichtung',
            options={'managed': True, 'verbose_name': 'Einrichtung', 'verbose_name_plural': 'Einrichtungen'},
        ),
        migrations.AlterModelOptions(
            name='ferien',
            options={'managed': True, 'verbose_name': 'Ferien', 'verbose_name_plural': 'Ferien'},
        ),
        migrations.AlterModelOptions(
            name='gruppe',
            options={'managed': True, 'verbose_name': 'Gruppe', 'verbose_name_plural': 'Gruppen'},
        ),
        migrations.AlterModelOptions(
            name='schliesstag',
            options={'managed': True, 'verbose_name': 'Schliesstag', 'verbose_name_plural': 'Schliesstage'},
        ),
        migrations.AlterModelOptions(
            name='schueler',
            options={'managed': True, 'verbose_name': 'Schueler', 'verbose_name_plural': 'Schueler'},
        ),
        migrations.AlterModelOptions(
            name='sozialamt',
            options={'managed': True, 'verbose_name': 'Sozialamt', 'verbose_name_plural': 'Sozialaemter'},
        ),
        migrations.AlterModelOptions(
            name='stufe',
            options={'managed': True, 'verbose_name': 'Stufe', 'verbose_name_plural': 'Stufen'},
        ),
    ]
