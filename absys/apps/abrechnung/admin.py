from django.contrib import admin

from . import models

from import_export.admin import ImportExportActionModelAdmin


class RechnungAdmin(admin.TabularInline):
    model = models.Rechnung


#class RechnungsPositionAdmin(admin.ModelAdmin):
#    model = models.RechnungsPosition


class RechnungSozialamtAdmin(ImportExportActionModelAdmin):
#    model = models.RechnungSozialamt

    #raw_id_fields = ('nummer',)

    list_display = ('sozialamt', 'startdatum', 'enddatum')
    inlines = [
        RechnungAdmin,
    ]


admin.site.register(models.Rechnung)
#admin.site.register(models.RechnungsPosition, RechnungsPositionAdmin)
admin.site.register(models.RechnungSozialamt, RechnungSozialamtAdmin)