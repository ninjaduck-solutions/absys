from django.contrib import admin

from . import models

from import_export.admin import ImportExportActionModelAdmin

#TODO: dafuer sorgen, dass Zeilen richtig umgebrochen werden
class SchuelerInEinrichtungAdmin(admin.TabularInline):
    model = models.SchuelerInEinrichtung
    raw_id_fields = ('schueler',)


class EinrichtungHatPflegesatzAdmin(admin.TabularInline):
    model = models.EinrichtungHatPflegesatz


class EinrichtungAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'kuerzel')
    inlines = [
        EinrichtungHatPflegesatzAdmin,
        SchuelerInEinrichtungAdmin,
    ]


admin.site.register(models.Einrichtung, EinrichtungAdmin)
admin.site.register(models.Ferien)
admin.site.register(models.Schliesstag)
