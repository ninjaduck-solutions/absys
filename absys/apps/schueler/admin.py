from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from . import models


class SchuelerAdmin(ImportExportActionModelAdmin):
    list_display = ('nachname', 'vorname', 'geburtsdatum', 'gruppe', 'inaktiv')
    list_display_links = ('nachname', 'vorname')
    list_filter = ('inaktiv', 'gruppe',)
    search_fields = ['vorname', 'nachname']



class SozialamtAdmin(admin.ModelAdmin):

    ordering = ('name',)


admin.site.register(models.Gruppe)
admin.site.register(models.Schueler, SchuelerAdmin)
admin.site.register(models.Sozialamt, SozialamtAdmin)
