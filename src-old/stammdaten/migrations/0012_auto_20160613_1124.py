# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0011_auto_20160613_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnwesenheitTTT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datum', models.DateField()),
                ('anwesenheit', models.CharField(max_length=1)),
                ('abgerechnet', models.BooleanField(default=False)),
                ('schueler', models.ForeignKey(to='stammdaten.Schueler')),
            ],
            options={
                'verbose_name': 'Anwesenheit eines Schueler in einer Einrichtung',
                'verbose_name_plural': 'Anwesenheiten der Schueler',
            },
        ),
        migrations.CreateModel(
            name='FehltageSchuelerErlaubt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wert', models.PositiveIntegerField(default=45)),
                ('startdatum', models.DateField()),
                ('enddatum', models.DateField()),
                ('schueler', models.ForeignKey(to='stammdaten.Schueler')),
            ],
            options={
                'verbose_name': 'Erlaubte Fehltage eines Schuelers',
                'verbose_name_plural': 'Erlaubte Fehltage von Schuelern',
            },
        ),
        migrations.AlterUniqueTogether(
            name='anwesenheitttt',
            unique_together=set([('schueler', 'datum', 'abgerechnet')]),
        ),
    ]
