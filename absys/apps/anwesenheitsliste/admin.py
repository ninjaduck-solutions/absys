from django.contrib import admin

from . import models


class AnwesenheitAdmin(admin.ModelAdmin):
    list_display = ('schueler', 'einrichtung', 'datum', 'abwesend')
    list_display_links = ('schueler', 'einrichtung')
    list_editable = ['abwesend']


admin.site.register(models.Anwesenheit, AnwesenheitAdmin)
