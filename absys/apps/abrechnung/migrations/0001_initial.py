# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anwesenheit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('datum', models.DateField()),
                ('anwesenheit', models.CharField(max_length=1)),
                ('abgerechnet', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Anwesenheit eines Schueler in einer Einrichtung',
                'verbose_name_plural': 'Anwesenheiten der Schueler',
            },
        ),
        migrations.CreateModel(
            name='Einrichtung',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=15)),
                ('kuerzel', models.CharField(max_length=1)),
                ('pflegesatz', models.DecimalField(decimal_places=2, max_digits=4)),
                ('pflegesatz_startdatum', models.DateField()),
                ('pflegesatz_enddatum', models.DateField()),
                ('pflegesatz_ferien', models.DecimalField(decimal_places=2, max_digits=4)),
                ('pflegesatz_ferien_startdatum', models.DateField()),
                ('pflegesatz_ferien_enddatum', models.DateField()),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Einrichtung',
                'verbose_name_plural': 'Einrichtungen',
            },
        ),
        migrations.CreateModel(
            name='FehltageSchuelerErlaubt',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('wert', models.PositiveIntegerField(default=45)),
                ('startdatum', models.DateField()),
                ('enddatum', models.DateField()),
            ],
            options={
                'verbose_name': 'Erlaubte Fehltage eines Schuelers',
                'verbose_name_plural': 'Erlaubte Fehltage von Schuelern',
            },
        ),
        migrations.CreateModel(
            name='Ferien',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('startdatum', models.DateField()),
                ('enddatum', models.DateField()),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
                ('einrichtungen', models.ManyToManyField(to='abrechnung.Einrichtung', verbose_name='Einrichtungen', related_name='ferien')),
            ],
            options={
                'verbose_name': 'Ferien',
                'verbose_name_plural': 'Ferien',
            },
        ),
        migrations.CreateModel(
            name='Gruppe',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(default='', max_length=5)),
                ('bemerkungen', models.CharField(max_length=200)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Gruppe',
                'verbose_name_plural': 'Gruppen',
            },
        ),
        migrations.CreateModel(
            name='Schliesstag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('datum', models.DateField()),
                ('art', models.CharField(blank=True, max_length=10)),
                ('name', models.CharField(blank=True, max_length=5)),
                ('einrichtungen', models.ManyToManyField(to='abrechnung.Einrichtung', verbose_name='Einrichtungen', related_name='schliesstage')),
            ],
            options={
                'verbose_name': 'Schliesstag',
                'verbose_name_plural': 'Schliesstage',
            },
        ),
        migrations.CreateModel(
            name='Schueler',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nachname', models.CharField(max_length=10)),
                ('vorname', models.CharField(max_length=10)),
                ('geburtsdatum', models.DateField()),
                ('bemerkungen', models.TextField(max_length=100)),
                ('buchungsnummer', models.CharField(blank=True, max_length=13)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Schueler',
                'verbose_name_plural': 'Schueler',
            },
        ),
        migrations.CreateModel(
            name='SchuelerInEinrichtung',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('eintritt', models.DateField()),
                ('austritt', models.DateField()),
                ('sozialamtbescheid_von', models.DateField()),
                ('sozialamtbescheid_bis', models.DateField()),
                ('pers_pflegesatz', models.DecimalField(default=0, decimal_places=2, max_digits=4)),
                ('pers_pflegesatz_startdatum', models.DateField(blank=True, null=True)),
                ('pers_pflegesatz_enddatum', models.DateField(blank=True, null=True)),
                ('pers_pflegesatz_ferien', models.DecimalField(default=0, decimal_places=2, max_digits=4)),
                ('pers_pflegesatz_ferien_startdatum', models.DateField(blank=True, null=True)),
                ('pers_pflegesatz_ferien_enddatum', models.DateField(blank=True, null=True)),
                ('einrichtung', models.ForeignKey(to='abrechnung.Einrichtung')),
                ('schueler', models.ForeignKey(to='abrechnung.Schueler')),
            ],
            options={
                'verbose_name': 'Schueler in der Einrichtung',
                'verbose_name_plural': 'Schueler in den Einrichtungen',
                'ordering': ('schueler__nachname', 'schueler__vorname', '-austritt'),
            },
        ),
        migrations.CreateModel(
            name='Sozialamt',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(default='', max_length=10)),
                ('anschrift', models.CharField(max_length=20)),
                ('konto_iban', models.CharField(max_length=22)),
                ('konto_institut', models.CharField(max_length=10)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Sozialamt',
                'verbose_name_plural': 'Sozialaemter',
            },
        ),
        migrations.CreateModel(
            name='Stufe',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(default='', max_length=5)),
                ('bemerkungen', models.CharField(max_length=200)),
                ('erstellungsdatum', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Stufe',
                'verbose_name_plural': 'Stufen',
            },
        ),
        migrations.AddField(
            model_name='schueler',
            name='einrichtungen',
            field=models.ManyToManyField(to='abrechnung.Einrichtung', through='abrechnung.SchuelerInEinrichtung'),
        ),
        migrations.AddField(
            model_name='schueler',
            name='gruppe',
            field=models.ForeignKey(to='abrechnung.Gruppe'),
        ),
        migrations.AddField(
            model_name='schueler',
            name='sozialamt',
            field=models.ForeignKey(to='abrechnung.Sozialamt'),
        ),
        migrations.AddField(
            model_name='schueler',
            name='stufe',
            field=models.ForeignKey(to='abrechnung.Stufe'),
        ),
        migrations.AddField(
            model_name='fehltageschuelererlaubt',
            name='schueler',
            field=models.ForeignKey(to='abrechnung.Schueler'),
        ),
        migrations.AddField(
            model_name='anwesenheit',
            name='schueler',
            field=models.ForeignKey(to='abrechnung.Schueler'),
        ),
        migrations.AlterUniqueTogether(
            name='schuelerineinrichtung',
            unique_together=set([('schueler', 'einrichtung', 'eintritt', 'austritt')]),
        ),
        migrations.AlterUniqueTogether(
            name='anwesenheit',
            unique_together=set([('schueler', 'datum', 'abgerechnet')]),
        ),
    ]
