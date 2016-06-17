from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Schueler)
admin.site.register(Gruppe)
admin.site.register(Stufe)