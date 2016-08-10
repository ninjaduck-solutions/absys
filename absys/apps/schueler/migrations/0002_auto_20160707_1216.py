# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schueler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schueler',
            name='gruppe',
            field=models.ForeignKey(related_name='schueler', to='schueler.Gruppe'),
        ),
        migrations.AlterField(
            model_name='schueler',
            name='sozialamt',
            field=models.ForeignKey(related_name='schueler', to='schueler.Sozialamt'),
        ),
        migrations.AlterField(
            model_name='schueler',
            name='stufe',
            field=models.ForeignKey(related_name='schueler', to='schueler.Stufe'),
        ),
    ]
