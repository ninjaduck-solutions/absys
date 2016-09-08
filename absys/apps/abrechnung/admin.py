from django.contrib import admin

from . import models

from import_export.admin import ImportExportActionModelAdmin


class RechnungSchuelerInline(admin.TabularInline):
    model = models.RechnungSchueler


class RechnungSozialamtAdmin(ImportExportActionModelAdmin):

    list_display = ('sozialamt', 'startdatum', 'enddatum')
    inlines = [
        RechnungSchuelerInline,
    ]


admin.site.register(models.RechnungSchueler)
admin.site.register(models.RechnungsPositionSchueler)
admin.site.register(models.RechnungSozialamt, RechnungSozialamtAdmin)
