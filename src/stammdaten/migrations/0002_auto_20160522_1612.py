# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='einrichtung',
            options={'managed': True, 'verbose_name_plural': 'Einrichtungen'},
        ),
        migrations.AlterModelOptions(
            name='ferientag',
            options={'managed': True, 'verbose_name_plural': 'Ferientage'},
        ),
        migrations.AlterModelOptions(
            name='gruppe',
            options={'managed': True, 'verbose_name_plural': 'Gruppen'},
        ),
        migrations.AlterModelOptions(
            name='schliesstag',
            options={'managed': True, 'verbose_name_plural': 'Schliesstage'},
        ),
        migrations.AlterModelOptions(
            name='schueler',
            options={'managed': True, 'verbose_name_plural': 'Schueler'},
        ),
        migrations.AlterModelOptions(
            name='schuelerineinrichtung',
            options={'managed': True, 'verbose_name': 'Schueler in der Einrichtung', 'verbose_name_plural': 'Schueler in der Einrichtung'},
        ),
        migrations.AlterModelOptions(
            name='sozialamt',
            options={'managed': True, 'verbose_name_plural': 'Sozialaemter'},
        ),
        migrations.AlterModelOptions(
            name='stufe',
            options={'managed': True, 'verbose_name_plural': 'Stufen'},
        ),
    ]
