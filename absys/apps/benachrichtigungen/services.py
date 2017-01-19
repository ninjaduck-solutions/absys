import datetime

from django.conf import settings
from django.utils.timezone import now

from absys.apps.einrichtungen.models import (SchuelerInEinrichtung, EinrichtungHatPflegesatz,
                                             Bettengeldsatz, Einrichtung)
from . import models


def pruefe_schueler_in_einrichtung():
    """
    Erstelle Benachrichtigungen über auslaufende ``SchuelerInEinrichung`` Instanzen.

    Note:
        Wir berücksichtigen hierfür nur solche ``SchuelerInEinrichtung``en welche noch
        nicht 'abgelaufen' sind, d.h wo ``SchuelerInEinrichtung.austritt >= heute``.
    """

    def pruefe_eintrag(eintrag):
        """
        Prüfe ob für eine ``SchuelerInEinrichtung`` eine Benachrichtigung ausgelöst werden soll.

        Ein ``eintrag`` soll nach Spezifikation eine Benachrichtigung auslösen wenn:
        1. ``eintrag.austritt`` weniger als die im Schwellwert genannte Anzahl an Tagen
            'entfernt' ist. Oder,
        2. ``eintrag`` ein ``pers_pflegesatz_enddatum`` hat welches nur noch weniger als die
            geforderte Anzahl entfernt ist.

        Returns:
            bool: ``False`` wenn ``eintrag`` unter Schwellwert liegt.
        """
        schwellwert = settings.ABSYS_EINRICHTUNG_MIN_VERBLEIBENDE_TAGE

        if (eintrag.austritt - heute) < datetime.timedelta(schwellwert):
            result = False
        # Wir hätten hier auch mit ``or`` verknüpfen können, aber so sind die
        # Zeilen übersichtlicher.
        elif eintrag.pers_pflegesatz_enddatum and (
            (eintrag.pers_pflegesatz_enddatum - heute) < datetime.timedelta(schwellwert)
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
    """
    Erstelle Benachrichtigungen über auslaufende ``EinrichtungHatPflegesatz`` Instanzen.

    Note:
        Wir berücksichtigen hierfür nur solche ``EinrichtungHatPflegesatz``en welche noch
        nicht 'abgelaufen' sind, d.h wo ``EinrichtungHatPflegesatz.pflegesatz_enddatum >= heute``.
    """
    def pruefe_eintrag(eintrag):
        """
        Prüfe ob für eine ``EinrichtungHatPflegesatz`` eine Benachrichtigung ausgelöst werden soll.

        Ein ``eintrag`` soll nach Spezifikation eine Benachrichtigung auslösen wenn
        ``eintrag.pflegesatz_enddatum`` weniger als die im Schwellwert genannte Anzahl an Tagen
        'entfernt' ist.

        Returns:
            bool: ``False`` wenn ``eintrag`` unter Schwellwert liegt.
        """
        schwellwert = settings.ABSYS_EINRICHTUNG_HAT_PFLEGESATZ_MIN_VERBLEIBENDE_TAGE
        return not (eintrag.pflegesatz_enddatum - heute) < datetime.timedelta(schwellwert)

    heute = datetime.date.today()
    for eintrag in EinrichtungHatPflegesatz.objects.filter(pflegesatz_enddatum__gte=heute):
        if not pruefe_eintrag(eintrag):
            models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects.benachrichtige(
                eintrag
            )


def pruefe_bettengeldsatz():
    """
    Erstelle Benachrichtigungen über auslaufende ``Bettengeldsatz`` Instanzen.

    Note:
        Wir berücksichtigen hierfür nur solche ``Bettengeldsatz``e welche noch
        nicht 'abgelaufen' sind, d.h wo ``Bettengeldsatz.enddatum >= heute``.
    """
    def pruefe_eintrag(eintrag):
        """
        Prüfe ob für einen ``Bettengeldsatz`` eine Benachrichtigung ausgelöst werden soll.

        Ein ``eintrag`` soll nach Spezifikation eine Benachrichtigung auslösen wenn
        ``eintrag.enddatum`` weniger als die im Schwellwert genannte Anzahl an Tagen
        'entfernt' ist.

        Returns:
            bool: ``False`` wenn ``eintrag`` unter Schwellwert liegt.
        """
        schwellwert = settings.ABSYS_BETTENGELDSATZ_MIN_VERBLEIBENDE_TAGE
        return not (eintrag.enddatum - heute) < datetime.timedelta(schwellwert)

    heute = datetime.date.today()
    for eintrag in Bettengeldsatz.objects.filter(enddatum__gte=heute):
        if not pruefe_eintrag(eintrag):
            models.BettengeldsatzLaeuftAusBenachrichtigung.objects.benachrichtige(eintrag)


def pruefe_ferien():
    """Erstelle Benachrichtigungen für alle Einrichtungen ohne Ferien im aktuellen Jahr."""

    jahr = now().year
    for eintrag in Einrichtung.objects.all():
        if not eintrag.ferien.jahr(jahr):
            models.FerienBenachrichtigung.objects.benachrichtige(eintrag, jahr)


def pruefe_schliesstage():
    """Erstelle Benachrichtigungen für alle Einrichtungen ohne Schliesstage im aktuellen Jahr."""
    jahr = now().year
    for eintrag in Einrichtung.objects.all():
        if not eintrag.schliesstage.filter(datum__year=jahr):
            models.SchliesstageBenachrichtigung.objects.benachrichtige(eintrag, jahr)
