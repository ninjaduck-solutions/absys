from django.contrib import admin

from . import models

from import_export.admin import ImportExportActionModelAdmin


class SchuelerInEinrichtungAdmin(admin.ModelAdmin):
    date_hierarchy = 'eintritt'
    list_display = ('schueler', 'einrichtung', 'eintritt', 'austritt', 'fehltage_erlaubt')
    list_filter = ('einrichtung',)
    raw_id_fields = ('schueler',)


#TODO: dafuer sorgen, dass Zeilen richtig umgebrochen werden
class SchuelerInEinrichtungInline(admin.TabularInline):
    model = models.SchuelerInEinrichtung
    raw_id_fields = ('schueler',)
    extra = 0


class EinrichtungHatPflegesatzAdmin(admin.TabularInline):
    model = models.EinrichtungHatPflegesatz
    extra = 0


class EinrichtungAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'kuerzel')
    inlines = [
        EinrichtungHatPflegesatzAdmin,
        SchuelerInEinrichtungInline,
    ]


admin.site.register(models.SchuelerInEinrichtung, SchuelerInEinrichtungAdmin)
admin.site.register(models.Einrichtung, EinrichtungAdmin)
admin.site.register(models.Ferien)
admin.site.register(models.Schliesstag)
