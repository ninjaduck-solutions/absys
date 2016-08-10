# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FehltageSchuelerErlaubt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('wert', models.PositiveIntegerField(default=45)),
                ('startdatum', models.DateField()),
                ('enddatum', models.DateField()),
                ('jahr', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Erlaubte Fehltage eines Schülers',
                'verbose_name_plural': 'Erlaubte Fehltage von Schülern',
            },
        ),
        migrations.CreateModel(
            name='Gruppe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('bemerkungen', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Gruppe',
                'verbose_name_plural': 'Gruppen',
            },
        ),
        migrations.CreateModel(
            name='Schueler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('vorname', models.CharField(verbose_name='Vorname', max_length=30)),
                ('nachname', models.CharField(verbose_name='Nachname', max_length=30)),
                ('geburtsdatum', models.DateField()),
                ('bemerkungen', models.TextField(blank=True)),
                ('buchungsnummer', models.CharField(max_length=13, blank=True)),
                ('gruppe', models.ForeignKey(to='schueler.Gruppe')),
            ],
            options={
                'verbose_name': 'Schüler',
                'verbose_name_plural': 'Schüler',
                'ordering': ['nachname', 'vorname'],
            },
        ),
        migrations.CreateModel(
            name='Sozialamt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('anschrift', models.TextField()),
                ('konto_iban', models.CharField(max_length=22)),
                ('konto_institut', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Sozialamt',
                'verbose_name_plural': 'Sozialämter',
            },
        ),
        migrations.CreateModel(
            name='Stufe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('bemerkungen', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Stufe',
                'verbose_name_plural': 'Stufen',
            },
        ),
        migrations.AddField(
            model_name='schueler',
            name='sozialamt',
            field=models.ForeignKey(to='schueler.Sozialamt'),
        ),
        migrations.AddField(
            model_name='schueler',
            name='stufe',
            field=models.ForeignKey(to='schueler.Stufe'),
        ),
        migrations.AddField(
            model_name='fehltageschuelererlaubt',
            name='schueler',
            field=models.ForeignKey(to='schueler.Schueler'),
        ),
    ]
