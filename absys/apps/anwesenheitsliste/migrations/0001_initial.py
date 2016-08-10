# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0001_initial'),
        ('schueler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anwesenheit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('datum', models.DateField(verbose_name='Datum')),
                ('abwesend', models.BooleanField(verbose_name='Abwesend', default=False)),
                ('einrichtung', models.ForeignKey(verbose_name='Einrichtung', to='einrichtungen.Einrichtung')),
                ('schueler', models.ForeignKey(related_name='anwesenheit', verbose_name='Schüler', to='schueler.Schueler')),
            ],
            options={
                'verbose_name': 'Anwesenheit',
                'verbose_name_plural': 'Anwesenheiten',
                'ordering': ['datum', 'schueler'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='anwesenheit',
            unique_together=set([('schueler', 'einrichtung', 'datum')]),
        ),
    ]
