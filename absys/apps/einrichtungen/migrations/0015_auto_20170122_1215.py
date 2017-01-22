# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-22 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0014_auto_20170122_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz',
            field=models.DecimalField(decimal_places=2, default=0, help_text="Wenn der Schüler keinen persönlichen Pflegesatz zugewiesen bekommen hat, muss in diesem Feld '0' stehen bleiben.", max_digits=5, verbose_name='Persönlicher Pflegesatz'),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='pers_pflegesatz_ferien',
            field=models.DecimalField(decimal_places=2, default=0, help_text="Wenn der Schüler keinen persönlichen Pflegesatz für Ferien zugewiesen bekommen hat, muss in diesem Feld '0' stehen bleiben.", max_digits=5, verbose_name='Persönlicher Pflegesatz Ferien'),
        ),
    ]
