# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anwesenheit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('anwesend', models.BooleanField(default=True)),
                ('datum', models.DateField(default=django.utils.timezone.now)),
                ('schueler', models.ForeignKey(to='stammdaten.Schueler')),
            ],
            options={
                'verbose_name': 'Anwesenheit',
                'verbose_name_plural': 'Anwesenheiten',
            },
        ),
        migrations.AlterUniqueTogether(
            name='anwesenheit',
            unique_together=set([('schueler', 'datum')]),
        ),
    ]
