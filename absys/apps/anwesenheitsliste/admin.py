from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget

from . import models
from absys.apps.schueler.models import Schueler



class AnwesenheitenResource(resources.ModelResource):

    #schueler = fields.Field(column_name='schueler', attribute='schueler', widget=ForeignKeyWidget(Schueler, 'pk'))

    class Meta:

        model = models.Anwesenheit

        # fields = (
        #     'id',
        #     'datum',
        #     'schueler',
        #     'einrichtung',
        #     'abwesend',
        #     )

class AnwesenheitAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):

    list_display = ('schueler', 'datum', 'abwesend')
    list_display_links = ('schueler',)
    list_editable = ['abwesend']
    list_filter = ('datum', 'schueler')
    search_fields = ['schueler__nachname', 'schueler__vorname', 'datum']

    resource_class = AnwesenheitenResource


admin.site.register(models.Anwesenheit, AnwesenheitAdmin)
