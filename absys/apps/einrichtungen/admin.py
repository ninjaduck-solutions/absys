from django.contrib import admin

from . import models


class EinrichtungAdmin(admin.ModelAdmin):
    list_display = ('name', 'kuerzel')


admin.site.register(models.Einrichtung, EinrichtungAdmin)
