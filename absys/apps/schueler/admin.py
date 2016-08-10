from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from . import models


#class SchuelerResource(resources.ModelResource):
#
#    class Meta:
#        model = models.Schueler

class SchuelerAdmin(ImportExportModelAdmin):
    list_display = ('nachname', 'vorname', 'geburtsdatum', 'stufe', 'gruppe')
    list_display_links = ('nachname', 'vorname')
    list_filter = ('stufe', 'gruppe')
    search_fields = ['vorname', 'nachname']

class SchuelerAdmin(ImportExportActionModelAdmin):
    pass

admin.site.register(models.Gruppe)
admin.site.register(models.Schueler, SchuelerAdmin)
admin.site.register(models.Sozialamt)
admin.site.register(models.Stufe)
