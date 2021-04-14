from django.utils import timezone

from django.contrib import admin

from django.db.models import Q

from . import models

from import_export.admin import ImportExportActionModelAdmin


# class HeuteAngemeldetListFilter(admin.SimpleListFilter):
#     title = 'Zeitraum'
#     parameter_name = 'angemeldet'


#     def lookups(self, request, model_admin):
#         fruehestes = queryset.objects.order_by('eintritt').first().eintritt.year
#         spaetestes = queryset.objects.order_by('austritt').last().austritt.year


#         return (
#             ('heute', 'heute'),
#             ('aktueller Monat', 'aktueller Monat: noch nicht fertig'),
#             ('aktuelles Jahr', 'aktuelles Jahr'),
#             (
#                 for jahre in range(fruehestes, spaetestes):
#                     #TODO: mit automatischem Filter weitermachen
#             ),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == 'heute':
#             return queryset.war_angemeldet(timezone.now().date())
#         if self.value() == 'aktueller Monat':
#             return queryset.filter(
#                 Q(eintritt__year=timezone.now().year) &
#                 Q(eintritt__month=timezone.now().month)
#             )
#         if self.value() == 'aktuelles Jahr':
#             return queryset.filter(
#                 Q(eintritt__year__lte=timezone.now().year) &
#                 Q(austritt__year__gte=timezone.now().year)
#             )


class SchuelerInEinrichtungAdmin(admin.ModelAdmin):
    date_hierarchy = 'eintritt'
    fields = ('schueler', 'einrichtung', 'eintritt', 'austritt', 'pers_pflegesatz',
        'pers_pflegesatz_ferien', 'pers_pflegesatz_startdatum', 'pers_pflegesatz_enddatum',
        'fehltage_berechnet', 'fehltage_erlaubt', 'anteile_bargeld', 'sozialamt')
    list_display = ('schueler', 'einrichtung', 'sozialamt', 'eintritt', 'austritt', 'fehltage_erlaubt',)
    list_filter = ('einrichtung', 'sozialamt',)
    raw_id_fields = ('schueler',)
    readonly_fields = ('sozialamt', 'fehltage_berechnet')
    search_fields = ['schueler__nachname', 'schueler__vorname', 'sozialamt__name',]


class EinrichtungHatPflegesatzAdmin(admin.TabularInline):
    model = models.EinrichtungHatPflegesatz
    extra = 0


class BettengeldsatzInlineAdmin(admin.TabularInline):
    model = models.Bettengeldsatz
    fields = ('satz', 'startdatum', 'enddatum')
    extra = 0


class EinrichtungAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'kuerzel')
    inlines = [
        EinrichtungHatPflegesatzAdmin, BettengeldsatzInlineAdmin
    ]


admin.site.register(models.SchuelerInEinrichtung, SchuelerInEinrichtungAdmin)
admin.site.register(models.Einrichtung, EinrichtungAdmin)
admin.site.register(models.Ferien)
admin.site.register(models.Schliesstag)
admin.site.register(models.Standort)
admin.site.register(models.Bargeldsatz)
