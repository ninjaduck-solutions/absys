from django.contrib import admin

from . import models

from import_export.admin import ImportExportActionModelAdmin


class RechnungInline(admin.TabularInline):
    model = models.Rechnung


class RechnungSozialamtAdmin(ImportExportActionModelAdmin):

    list_display = ('sozialamt', 'startdatum', 'enddatum')
    inlines = [
        RechnungInline,
    ]


admin.site.register(models.Rechnung)
admin.site.register(models.RechnungsPosition)
admin.site.register(models.RechnungSozialamt, RechnungSozialamtAdmin)
