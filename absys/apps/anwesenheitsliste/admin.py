from django.contrib import admin

from import_export import resources, fields

from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget

from . import models

from absys.apps.schueler.models import Schueler
from absys.apps.einrichtungen.models import Einrichtung



class AnwesenheitenResource(resources.ModelResource):

#Warum benötigen wir bei der Anwesenheitserfassung die Einrichtung? SchuelerInEinrichtung-Sets können sich nicht mehr zeitlich pro Schüler überlappen

    class Meta:

        model = models.Anwesenheit

        import_id_fields = (
            'schueler__nachname',
            'schueler__geburtsdatum',
            'datum',
            )

        fields = (
            'datum',
            'schueler__nachname',
            'schueler__geburtsdatum',
            'abwesend',
            )

        export_order = (
            'datum',
            'schueler__nachname',
            'schueler__geburtsdatum',
            'abwesend',
            )

class AnwesenheitAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):

    list_display = ('schueler', 'einrichtung', 'datum', 'abwesend')
    list_display_links = ('schueler', 'einrichtung')
    list_editable = ['abwesend']
    list_filter = ('datum', 'schueler')
    search_fields = ['schueler__nachname', 'schueler__vorname', 'einrichtung__name', 'datum']

    resource_class = AnwesenheitenResource


admin.site.register(models.Anwesenheit, AnwesenheitAdmin)