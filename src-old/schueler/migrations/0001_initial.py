# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gruppe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gruppenname', models.CharField(default=b'1', max_length=400)),
                ('bemerkungen', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Schueler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nachname', models.CharField(max_length=200)),
                ('vorname', models.CharField(max_length=200)),
                ('geburtsdatum', models.DateTimeField()),
                ('bemerkungen', models.TextField(max_length=10000)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
                ('gruppe', models.ForeignKey(default=b'1', to='schueler.Gruppe')),
            ],
        ),
        migrations.CreateModel(
            name='Stufe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stufenname', models.CharField(default=b'1', max_length=400)),
                ('bemerkungen', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='schueler',
            name='stufe',
            field=models.ForeignKey(default=b'1', to='schueler.Stufe'),
        ),
    ]
