from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Gruppe)
admin.site.register(Stufe)
admin.site.register(Einrichtung)
admin.site.register(Sozialamt)
admin.site.register(Schliesstag)
admin.site.register(Ferien)
admin.site.register(Schueler)
admin.site.register(SchuelerInEinrichtung)