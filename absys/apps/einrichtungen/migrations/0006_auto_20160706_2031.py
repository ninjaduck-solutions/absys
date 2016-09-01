# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('einrichtungen', '0005_auto_20160706_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='austritt',
            field=models.DateField(verbose_name='Austritt', help_text='Der Austritt muss nach dem Eintritt erfolgen.'),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='eintritt',
            field=models.DateField(verbose_name='Eintritt'),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='sozialamtbescheid_bis',
            field=models.DateField(verbose_name='Sozialamtbescheid bis', help_text='Das Endes des Sozialamtbescheides muss nach dem Beginn erfolgen.'),
        ),
        migrations.AlterField(
            model_name='schuelerineinrichtung',
            name='sozialamtbescheid_von',
            field=models.DateField(verbose_name='Sozialamtbescheid von'),
        ),
    ]
