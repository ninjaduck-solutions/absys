# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-21 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abrechnung', '0014_auto_20160920_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rechnungspositioneinrichtung',
            name='name_schueler',
            field=models.CharField(max_length=62, verbose_name='Name des Schülers'),
        ),
        migrations.AlterField(
            model_name='rechnungspositionschueler',
            name='name_schueler',
            field=models.CharField(max_length=62, verbose_name='Name des Schülers'),
        ),
    ]