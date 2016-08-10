from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from . import models


class AnwesenheitenResource(resources.ModelResource):

    class Meta:
    	model = models.Anwesenheit
    	fields = (
    		'schueler__vorname', 
    		'schueler__nachname', 
    		'schueler__buchungsnummer',
    		'einrichtung__name',
    		)


class AnwesenheitAdmin(ImportExportActionModelAdmin):

    list_display = ('schueler', 'einrichtung', 'datum', 'abwesend')
    list_display_links = ('schueler', 'einrichtung')
    list_editable = ['abwesend']

    resource_class = AnwesenheitenResource

admin.site.register(models.Anwesenheit, AnwesenheitAdmin)
