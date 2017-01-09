from django.db import models
from django.conf import settings
from . import managers
from absys.apps.einrichtungen.models import (SchuelerInEinrichtung, EinrichtungHatPflegesatz,
                                             Bettengeldsatz, Einrichtung)


class Benachrichtigung(models.Model):
    """Eine *persistente* Userbenachrichtigung."""

    erstellt = models.DateTimeField(auto_now_add=True)
    erledigt = models.BooleanField(default=False)
    text = models.TextField()

    def __str__(self):
        return '{text} ({s.erstellt}) ({s.erledigt})'.format(text=self.text[:25], s=self)


class BuchungskennzeichenBenachrichtigung(Benachrichtigung):
    objects = managers.BuchungskennzeichenBenachrichtigungManager()

    def _settext(self):
        self.text = (
            "Es verbleiben weniger als {} Buchungskennzeichen. Bitte tragen Sie"
            " baldestmöglich zusätzliche Buchungskennzeichen nach.".format(
                settings.ABSYS_BUCHUNGSKENNZEICHEN_MIN_VERBLEIBEND)
        )

    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)


class SchuelerInEinrichtungLaeuftAusBenachrichtigung(Benachrichtigung):
    schueler_in_einrichtung = models.ForeignKey(SchuelerInEinrichtung,
        related_name='auslauf_benachrichtigungen')
    objects = managers.SchuelerInEinrichtungLaeuftAusBenachrichtigungManager()

    def _settext(self):
        self.text = (
            "Für {i.schueler} läuft der aktuelle"
            " 'SchuelerInEinrichtung'-Zeitraum ab.".format(i=self.schueler_in_einrichtung)
        )

    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)


class EinrichtungHatPflegesatzLaeuftAusBenachrichtigung(Benachrichtigung):
    einrichtung_hat_pflegesatz = models.ForeignKey(EinrichtungHatPflegesatz,
        related_name='auslauf_benachrichtigungen')
    objects = managers.EinrichtungHatPflegesatzLaeuftAusBenachrichtigungManager()

    def _settext(self):
        self.text = (
            "'EinrichtungInPflegesatz' {} läuft aus.".format(self.einrichtung_hat_pflegesatz)
        )


    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)

class BettengeldsatzLaeuftAusBenachrichtigung(Benachrichtigung):
    bettengeldsatz = models.ForeignKey(Bettengeldsatz, related_name='auslauf_benachrichtigungen')
    objects = managers.BettengeldsatzLaeuftAusBenachrichtigungManager()

    def _settext(self):
        self.text = (
            "'Bettensatz [{}] läuft aus.".format(self.bettengeldsatz.pk)
        )


    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)

class FerienBenachrichtigung(Benachrichtigung):
    einrichtung = models.ForeignKey(Einrichtung, related_name='ferien_benachrichtigungen')
    jahr = models.IntegerField()
    objects = managers.FerienBenachrichtigungManager()

    def _settext(self):
        self.text = (
            "Für die Einrichtung {} wurden im laufenden Jahr noch keinerlei Ferien"
            "definiert.".format(self.einrichtung)
        )


    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)

class SchliesstageBenachrichtigung(Benachrichtigung):
    einrichtung = models.ForeignKey(Einrichtung, related_name='schliesstage_benachrichtigungen')
    jahr = models.IntegerField()
    objects = managers.FerienBenachrichtigungManager()

    def _settext(self):
        self.text = (
            "Für die Einrichtung {} wurden im laufenden Jahr noch keinerlei Schließtage"
            "definiert.".format(self.einrichtung)
        )

    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)
