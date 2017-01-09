from django.db import models
from django.conf import settings
from absys.apps.benachrichtigungen.models import BuchungskennzeichenBenachrichtigung


class BuchungskennzeichenManager(models.Manager):

    def benutzen(self):
        """
        Gibt das älteste verfügbare Buchungskennzeichen als Zeichenkette zurück.

        Das zurückgegebene Buchungskennzeichen ist danach nicht mehr verfügbar.
        """
        obj = self.filter(verfuegbar=True).order_by('-created').last()
        if obj is None:
            BuchungskennzeichenBenachrichtigung.objects.benachrichtige()
            return ''
        obj.verfuegbar = False
        obj.save()

        if self.filter(verfuegbar=True).count() < settings.ABSYS_BUCHUNGSKENNZEICHEN_MIN_VERBLEIBEND:
            BuchungskennzeichenBenachrichtigung.objects.benachrichtige()

        return obj.buchungskennzeichen
