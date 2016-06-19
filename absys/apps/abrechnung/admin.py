from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Gruppe)
admin.site.register(models.Stufe)
admin.site.register(models.Einrichtung)
admin.site.register(models.Ferien)
admin.site.register(models.Sozialamt)
admin.site.register(models.Schliesstag)
admin.site.register(models.Schueler)
admin.site.register(models.SchuelerInEinrichtung)
admin.site.register(models.Anwesenheit)
admin.site.register(models.FehltageSchuelerErlaubt)