from django.db import models


class BuchungskennzeichenManager(models.Manager):

    def benutzen(self):
        """
        Gibt das älteste verfügbare Buchungskennzeichen als Zeichenkette zurück.

        Das zurückgegebene Buchungskennzeichen ist danach nicht mehr verfügbar.
        """
        obj = self.filter(verfuegbar=True).order_by('-created').last()
        if obj is None:
            return ''
        obj.verfuegbar = False
        obj.save()
        return obj.buchungskennzeichen
