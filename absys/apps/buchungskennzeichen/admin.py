from django.contrib import admin
from django.utils.encoding import force_text
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from . import models
from . import resources


class VerfuegbarFilter(admin.SimpleListFilter):

    title = "ist verfügbar"
    parameter_name = 'verfuegbar'

    def lookups(self, request, model_admin):
        return (
            ('1', "Ja"),
            ('0', "Nein"),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(verfuegbar=False)
        if self.value() == '1':
            return queryset.filter(verfuegbar=True)

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}, []),
                'display': title,
            }


class BuchungskennzeichenAdmin(ImportExportModelAdmin):

    list_display = ('buchungskennzeichen', 'verfuegbar', 'created', 'modified')
    list_display_links = None
    list_editable = ('buchungskennzeichen',)
    list_filter = (VerfuegbarFilter,)
    resource_class = resources.BuchungskennzeichenResource
    search_fields = ['buchungskennzeichen']

    def changelist_view(self, request, extra_context=None):
        """
        Gibt den View zum Anzeigen der Listenansicht zurück.

        Aktiviert den 'ist verfügbar' Filter, wenn dieser nicht durch den
        Benutzer aktiviert wurde.
        """
        if VerfuegbarFilter.parameter_name not in request.GET:
            request.GET = request.GET.copy()
            request.GET[VerfuegbarFilter.parameter_name] = '1'
        return super().changelist_view(request, extra_context)

    def get_export_formats(self):
        return [base_formats.CSV, base_formats.XLS]

    def get_import_formats(self):
        return [base_formats.CSV, base_formats.XLS]


admin.site.register(models.Buchungskennzeichen, BuchungskennzeichenAdmin)
