from django.contrib import admin

from . import models


class SchuelerAdmin(admin.ModelAdmin):
    list_display = ('nachname', 'vorname', 'einrichtungs_art')
    list_display_links = ('nachname', 'vorname')
    list_editable = ['einrichtungs_art']
    list_filter = ('einrichtungs_art',)
    search_fields = ['vorname', 'nachname']


class EinrichtungsArtAdmin(admin.ModelAdmin):
    list_display = ('name', 'kuerzel')


admin.site.register(models.Schueler, SchuelerAdmin)
admin.site.register(models.EinrichtungsArt, EinrichtungsArtAdmin)
