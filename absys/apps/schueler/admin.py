from django.contrib import admin

from . import models


class SchuelerAdmin(admin.ModelAdmin):
    list_display = ('nachname', 'vorname', 'geburtsdatum')
    list_display_links = ('nachname', 'vorname')
    list_filter = ('einrichtungen',)
    search_fields = ['vorname', 'nachname']


admin.site.register(models.Schueler, SchuelerAdmin)
