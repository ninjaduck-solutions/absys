from django.contrib import admin

from . import models

#TODO: dafuer sorgen, dass Zeilen richtig umgebrochen werden
class SchuelerInEinrichtungAdmin(admin.TabularInline):
    model = models.SchuelerInEinrichtung


class EinrichtungHatPflegesatzAdmin(admin.TabularInline):
    model = models.EinrichtungHatPflegesatz


class EinrichtungAdmin(admin.ModelAdmin):
    list_display = ('name', 'kuerzel')
    inlines = [
        EinrichtungHatPflegesatzAdmin,
        SchuelerInEinrichtungAdmin,
    ]


admin.site.register(models.Einrichtung, EinrichtungAdmin)
admin.site.register(models.Ferien)
admin.site.register(models.Schliesstag)
