from django.contrib import admin

from . import models

from import_export.admin import ImportExportActionModelAdmin


class SchuelerInEinrichtungAdmin(admin.ModelAdmin):
    date_hierarchy = 'eintritt'
    list_display = ('schueler', 'einrichtung', 'eintritt', 'austritt', 'fehltage_erlaubt')
    list_filter = ('einrichtung',)
    raw_id_fields = ('schueler',)


class EinrichtungHatPflegesatzAdmin(admin.TabularInline):
    model = models.EinrichtungHatPflegesatz
    extra = 0


class EinrichtungAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'kuerzel')
    inlines = [
        EinrichtungHatPflegesatzAdmin,
    ]


admin.site.register(models.SchuelerInEinrichtung, SchuelerInEinrichtungAdmin)
admin.site.register(models.Einrichtung, EinrichtungAdmin)
admin.site.register(models.Ferien)
admin.site.register(models.Schliesstag)
