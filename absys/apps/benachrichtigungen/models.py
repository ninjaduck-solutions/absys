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
    """Benachrichtigung über auslaufende Buchungskennzeichen."""

    objects = managers.BuchungskennzeichenBenachrichtigungManager.from_queryset(
        managers.BuchungskennzeichenQuerySet)()

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
    """Benachrichtigung über auslaufenden Zeitraum für ``SchuelerInEinchrichtung`` Instanz."""

    schueler_in_einrichtung = models.ForeignKey(SchuelerInEinrichtung,
        related_name='auslauf_benachrichtigungen', on_delete=models.CASCADE)
    objects = managers.SchuelerInEinrichtungLaeuftAusBenachrichtigungManager.from_queryset(
        managers.SchuelerInEinrichtungLaeuftAusBenachrichtigungQuerySet)()

    def _settext(self):
        self.text = (
            "Für {i.schueler} läuft der aktuelle"
            " 'SchuelerInEinrichtung'-Zeitraum ab.".format(i=self.schueler_in_einrichtung)
        )

    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)


class EinrichtungHatPflegesatzLaeuftAusBenachrichtigung(Benachrichtigung):
    """Benachrichtigung über auslaufenden Zeitraum für ``EinrichtungHatPflegesatz`` Instanz."""

    einrichtung_hat_pflegesatz = models.ForeignKey(EinrichtungHatPflegesatz,
        related_name='auslauf_benachrichtigungen', on_delete=models.CASCADE)
    objects = managers.EinrichtungHatPflegesatzLaeuftAusBenachrichtigungManager.from_queryset(
        managers.EinrichtungHatPflegesatzLaeuftAusBenachrichtigungQuerySet)()

    def _settext(self):
        self.text = (
            "'EinrichtungInPflegesatz' {} läuft aus.".format(self.einrichtung_hat_pflegesatz)
        )

    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)


class BettengeldsatzLaeuftAusBenachrichtigung(Benachrichtigung):
    """Benachrichtigung über auslaufenden Zeitraum für ``Bettensatz`` Instanz."""

    bettengeldsatz = models.ForeignKey(Bettengeldsatz, related_name='auslauf_benachrichtigungen',
        on_delete=models.CASCADE)
    objects = managers.BettengeldsatzLaeuftAusBenachrichtigungManager.from_queryset(
        managers.BettengeldsatzLaeuftAusBenachrichtigungQuerySet)()

    def _settext(self):
        self.text = (
            "'Bettensatz [{}] läuft aus.".format(self.bettengeldsatz.pk)
        )

    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)


class FerienBenachrichtigung(Benachrichtigung):
    """Benachrichtigung das für ein bestimmtes Jahr noch keinerlei Ferien definiert wurden."""

    einrichtung = models.ForeignKey(Einrichtung, related_name='ferien_benachrichtigungen',
        on_delete=models.CASCADE)
    jahr = models.IntegerField()
    objects = managers.FerienBenachrichtigungManager.from_queryset(
        managers.FerienBenachrichtigungQuerySet)()

    def _settext(self):
        self.text = (
            "Für die Einrichtung {einrichtung} wurden für das Jahr {jahr} noch keinerlei Ferien"
            " definiert.".format(einrichtung=self.einrichtung, jahr=self.jahr)
        )

    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)


class SchliesstageBenachrichtigung(Benachrichtigung):
    """
    Benachrichtigung das für ein bestimmtes Jahr noch keinerlei Schliesstage definiert wurden.
    """
    einrichtung = models.ForeignKey(Einrichtung, related_name='schliesstage_benachrichtigungen',
        on_delete=models.CASCADE)
    jahr = models.IntegerField()
    objects = managers.SchliesstageBenachrichtigungManager.from_queryset(
        managers.SchliesstageBenachrichtigungQuerySet)()

    def _settext(self):
        self.text = (
            "Für die Einrichtung {einrichtung} wurden für das Jahr {jahr} noch keinerlei"
            " Schliesstage definiert.".format(einrichtung=self.einrichtung, jahr=self.jahr)
        )

    def save(self, *args, **kwargs):
        self._settext()
        super().save(*args, **kwargs)
