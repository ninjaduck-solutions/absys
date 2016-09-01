# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0006_auto_20160706_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='einrichtung',
            field=models.ForeignKey(related_name='anmeldungen', to='einrichtungen.Einrichtung'),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='schueler',
            field=models.ForeignKey(related_name='angemeldet_in_einrichtung', to='schueler.Schueler'),
        ),
    ]
