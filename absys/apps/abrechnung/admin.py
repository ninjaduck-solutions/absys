from django.contrib import admin

from . import models

from import_export.admin import ImportExportActionModelAdmin


class RechnungEinrichtungInline(admin.TabularInline):
    model = models.RechnungEinrichtung


class RechnungSozialamtAdmin(ImportExportActionModelAdmin):

    list_display = ('sozialamt', 'startdatum', 'enddatum')
    inlines = [
        RechnungEinrichtungInline,
    ]


admin.site.register(models.RechnungEinrichtung)
admin.site.register(models.RechnungsPositionEinrichtung)
admin.site.register(models.RechnungsPositionSchueler)
admin.site.register(models.RechnungSozialamt, RechnungSozialamtAdmin)
