from django.utils import timezone

from django.contrib import admin

from . import models

from import_export.admin import ImportExportActionModelAdmin


class HeuteAngemeldetListFilter(admin.SimpleListFilter):
    title = 'Zeitraum'
    parameter_name = 'angemeldet'

    def lookups(self, request, model_admin):
        return (
            ('heute', 'heute'),
            ('aktueller Monat', 'aktueller Monat - noch nicht fertig:'),
            ('aktuelles Jahr', 'aktuelles Jahr - noch nicht fertig'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'heute':
            return queryset.war_angemeldet(timezone.now().date())
        if self.value() == 'aktueller Monat':
            return queryset.filter(
                #TODO
                )
        if self.value() == 'aktuelles Jahr':
            return queryset.filter(
                #TODO
                )


class SchuelerInEinrichtungAdmin(admin.ModelAdmin):
    list_display = ('schueler', 'einrichtung', 'sozialamt', 'eintritt', 'austritt', 'fehltage_erlaubt')
    list_filter = (HeuteAngemeldetListFilter, 'einrichtung', 'sozialamt',)
    raw_id_fields = ('schueler',)
    readonly_fields = ('sozialamt',)


class EinrichtungHatPflegesatzAdmin(admin.TabularInline):
    model = models.EinrichtungHatPflegesatz
    extra = 0


class EinrichtungAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'kuerzel')
    inlines = [
        EinrichtungHatPflegesatzAdmin,
    ]

class StandortAdmin(admin.ModelAdmin):
    model = models.Standort


admin.site.register(models.SchuelerInEinrichtung, SchuelerInEinrichtungAdmin)
admin.site.register(models.Einrichtung, EinrichtungAdmin)
admin.site.register(models.Ferien)
admin.site.register(models.Schliesstag)
admin.site.register(models.Standort)
