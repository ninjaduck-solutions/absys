# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0012_auto_20160613_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anwesenheit',
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
        migrations.AlterUniqueTogether(
            name='anwesenheitttt',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='anwesenheitttt',
            name='schueler',
        ),
        migrations.DeleteModel(
            name='AnwesenheitTTT',
        ),
        migrations.AlterUniqueTogether(
            name='anwesenheit',
            unique_together=set([('schueler', 'datum', 'abgerechnet')]),
        ),
    ]
