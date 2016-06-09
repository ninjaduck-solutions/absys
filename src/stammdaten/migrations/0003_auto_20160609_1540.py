# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stammdaten', '0002_auto_20160609_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='FehltageErlaubt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('januar', models.IntegerField(default=4)),
                ('februar', models.IntegerField(default=8)),
                ('maerz', models.IntegerField(default=11)),
                ('april', models.IntegerField(default=15)),
                ('mai', models.IntegerField(default=19)),
                ('juni', models.IntegerField(default=23)),
                ('juli', models.IntegerField(default=26)),
                ('august', models.IntegerField(default=30)),
                ('september', models.IntegerField(default=34)),
                ('oktober', models.IntegerField(default=38)),
                ('november', models.IntegerField(default=41)),
                ('dezember', models.IntegerField(default=45)),
            ],
            options={
                'verbose_name': 'Erlaubte Fehltage',
                'verbose_name_plural': 'Erlaubte Fehltage',
            },
        ),
        migrations.AddField(
            model_name='schueler',
            name='fehltage_erlaubt',
            field=models.ForeignKey(default=1, to='stammdaten.FehltageErlaubt'),
            preserve_default=False,
        ),
    ]
