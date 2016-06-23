# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abrechnung', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fehltageschuelererlaubt',
            name='jahr',
            field=models.CharField(max_length=4, default='2016'),
            preserve_default=False,
        ),
    ]
