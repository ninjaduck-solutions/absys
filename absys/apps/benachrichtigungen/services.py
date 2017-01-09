import datetime

from django.conf import settings
from django.utils.timezone import now

from absys.apps.einrichtungen.models import (SchuelerInEinrichtung, EinrichtungHatPflegesatz,
                                             Bettengeldsatz, Einrichtung)
from . import models


def pruefe_schueler_in_einrichtung():
    def pruefe_eintrag(eintrag):
        """Returns False wenn eintrag unter threshold."""
        threshold = settings.ABSYS_EINRICHTUNG_MIN_VERBLEIBENDE_TAGE

        if (eintrag.austritt - heute) < datetime.timedelta(threshold):
            result = False
        # Wir hätten hier auch mit ``or`` verknüpfen können, aber so sind die
        # Zeilen übersichtlicher.
        elif eintrag.pers_pflegesatz_enddatum and (
            (eintrag.pers_pflegesatz_enddatum - heute) < datetime.timedelta(threshold)
        ):
            result = False
        else:
            result = True
        return result

    heute = datetime.date.today()
    for eintrag in SchuelerInEinrichtung.objects.filter(austritt__gte=heute):
        if not pruefe_eintrag(eintrag):
            models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects.benachrichtige(eintrag)


def pruefe_einrichtung_hat_pflegesatz():
    def pruefe_eintrag(eintrag):
        """Returns False wenn eintrag unter dem Schwellwert."""
        schwellwert = settings.ABSYS_EINRICHTUNG_HAT_PFLEGESATZ_MIN_VERBLEIBENDE_TAGE
        return not (eintrag.pflegesatz_enddatum - heute) < datetime.timedelta(schwellwert)

    heute = datetime.date.today()
    for eintrag in EinrichtungHatPflegesatz.objects.filter(pflegesatz_enddatum__gte=heute):
        if not pruefe_eintrag(eintrag):
            models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects.benachrichtige(eintrag)


def pruefe_bettengeldsatz():
    def pruefe_eintrag(eintrag):
        """Returns False wenn eintrag unter dem Schwellwert."""
        schwellwert = settings.ABSYS_BETTENGELDSATZ_MIN_VERBLEIBENDE_TAGE
        return not (eintrag.enddatum - heute) < datetime.timedelta(schwellwert)

    heute = datetime.date.today()
    for eintrag in Bettengeldsatz.objects.filter(enddatum__gte=heute):
        if not pruefe_eintrag(eintrag):
            models.BettengeldsatzLaeuftAusBenachrichtigung.objects.benachrichtige(eintrag)


def pruefe_ferien():
    def pruefe_eintrag(eintrag, jahr):
        """Returns False wenn keine ferien für den eintrag im gegebenem Jahr."""
        return bool(eintrag.ferien.jahr(jahr))

    jahr = now().year
    for eintrag in Einrichtung.objects.all():
        if not pruefe_eintrag(eintrag, jahr):
            models.FerienBenachrichtigung.objects.benachrichtige(eintrag, jahr)


def pruefe_schliesstage():
    def pruefe_eintrag(eintrag, jahr):
        """Returns False wenn keine ferien für den eintrag im gegebenem Jahr."""
        return bool(eintrag.schliesstage.filter(datum__year=jahr))

    jahr = now().year
    for eintrag in Einrichtung.objects.all():
        if not pruefe_eintrag(eintrag, jahr):
            models.SchliesstageBenachrichtigung.objects.benachrichtige(eintrag, jahr)
