# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abrechnung', '0002_fehltageschuelererlaubt_jahr'),
    ]

    operations = [
        migrations.CreateModel(
            name='EinrichtungHatPflegesatz',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('pflegesatz', models.DecimalField(max_digits=4, decimal_places=2)),
                ('pflegesatz_startdatum', models.DateField()),
                ('pflegesatz_enddatum', models.DateField()),
                ('pflegesatz_ferien', models.DecimalField(max_digits=4, decimal_places=2)),
                ('pflegesatz_ferien_startdatum', models.DateField()),
                ('pflegesatz_ferien_enddatum', models.DateField()),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Einrichtung',
                'verbose_name_plural': 'Einrichtungen',
            },
        ),
        migrations.RemoveField(
            model_name='einrichtung',
            name='erstellungsdatum',
        ),
        migrations.RemoveField(
            model_name='einrichtung',
            name='pflegesatz',
        ),
        migrations.RemoveField(
            model_name='einrichtung',
            name='pflegesatz_enddatum',
        ),
        migrations.RemoveField(
            model_name='einrichtung',
            name='pflegesatz_ferien',
        ),
        migrations.RemoveField(
            model_name='einrichtung',
            name='pflegesatz_ferien_enddatum',
        ),
        migrations.RemoveField(
            model_name='einrichtung',
            name='pflegesatz_ferien_startdatum',
        ),
        migrations.RemoveField(
            model_name='einrichtung',
            name='pflegesatz_startdatum',
        ),
        migrations.AddField(
            model_name='einrichtunghatpflegesatz',
            name='name',
            field=models.ForeignKey(to='abrechnung.Einrichtung'),
        ),
    ]
