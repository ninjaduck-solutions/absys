from django.contrib import admin
from django.conf import settings

from . import models

if settings.DEBUG:
    admin.site.register(models.BuchungskennzeichenBenachrichtigung)
    admin.site.register(models.SchuelerInEinrichtungLaeuftAusBenachrichtigung)
    admin.site.register(models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung)
