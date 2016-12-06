from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from . import models, resources


class AnwesenheitAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):

    date_hierarchy = 'datum'
    list_display = ('schueler', 'datum', 'abwesend')
    list_display_links = ('schueler',)
    list_editable = ['abwesend']
    list_filter = ('datum', 'schueler__gruppe__name', 'schueler',  )
    search_fields = ['schueler__nachname', 'schueler__vorname']

    resource_class = resources.AnwesenheitenResource


admin.site.register(models.Anwesenheit, AnwesenheitAdmin)
