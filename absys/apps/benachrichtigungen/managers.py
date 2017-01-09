from django.db import models


class BuchungskennzeichenBenachrichtigungManager(models.Manager):

    def benachrichtige(self):
        """Prüfe ob bereits eine unerledigte Benachrichtigung vorliegt, anderfalls erstelle eine."""
        if not self._vorhanden():
            self.create()

    def _vorhanden(self):
        """Liefert alle unerledigten instanzen."""
        return self.filter(erledigt=False)


class SchuelerInEinrichtungLaeuftAusBenachrichtigungManager(models.Manager):

    def benachrichtige(self, schueler_in_einrichtung):
        if not self._vorhanden(schueler_in_einrichtung):
            return self.create(schueler_in_einrichtung=schueler_in_einrichtung)

    def _vorhanden(self, schueler_in_einrichtung):
        """Liefert alle unerledigten instanzen mit 'identischen parametern'."""
        return self.filter(schueler_in_einrichtung=schueler_in_einrichtung, erledigt=False)


class EinrichtungHatPflegesatzLaeuftAusBenachrichtigungManager(models.Manager):

    def benachrichtige(self, einrichtung_hat_pflegesatz):
        if not self._vorhanden(einrichtung_hat_pflegesatz):
            return self.create(einrichtung_hat_pflegesatz=einrichtung_hat_pflegesatz)

    def _vorhanden(self, einrichtung_hat_pflegesatz):
        """Liefert alle unerledigten instanzen mit 'identischen parametern'."""
        return self.filter(einrichtung_hat_pflegesatz=einrichtung_hat_pflegesatz, erledigt=False)


class BettengeldsatzLaeuftAusBenachrichtigungManager(models.Manager):

    def benachrichtige(self, bettengeldsatz):
        if not self._vorhanden(bettengeldsatz):
            return self.create(bettengeldsatz=bettengeldsatz)

    def _vorhanden(self, bettengeldsatz):
        """Liefert alle unerledigten instanzen mit 'identischen parametern'."""
        return self.filter(bettengeldsatz=bettengeldsatz, erledigt=False)


class FerienBenachrichtigungManager(models.Manager):

    def benachrichtige(self, einrichtung, jahr):
        if not self._vorhanden(einrichtung, jahr):
            return self.create(einrichtung=einrichtung, jahr=jahr)

    def _vorhanden(self, einrichtung, jahr):
        """Liefert alle unerledigten instanzen mit 'identischen parametern'."""
        return self.filter(einrichtung=einrichtung, jahr=jahr, erledigt=False)


class SchliesstageBenachrichtigungManager(models.Manager):

    def benachrichtige(self, einrichtung, jahr):
        if not self._vorhanden(einrichtung, jahr):
            return self.create(einrichtung=einrichtung, jahr=jahr)

    def _vorhanden(self, einrichtung, jahr):
        """Liefert alle unerledigten instanzen mit 'identischen parametern'."""
        return self.filter(einrichtung=einrichtung, jahr=jahr, erledigt=False)
