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


class AnwesenheitAdmin(admin.ModelAdmin):
    list_display = ('schueler', 'einrichtungs_art', 'datum', 'abwesend')
    list_display_links = ('schueler', 'einrichtungs_art')
    list_editable = ['abwesend']


admin.site.register(models.Schueler, SchuelerAdmin)
admin.site.register(models.EinrichtungsArt, EinrichtungsArtAdmin)
admin.site.register(models.Anwesenheit, AnwesenheitAdmin)
