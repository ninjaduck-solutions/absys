from dateutil import relativedelta
from django.db import models


class SchuelerInEinrichtungQuerySet(models.QuerySet):

    def war_angemeldet(self, datum):
        return self.filter(
            eintritt__lte=datum,
            austritt__gte=datum
        )

    def zeitraum(self, startdatum, enddatum):
        """
        Gibt alle Objekte zurück, für die im angegebenen Zeitraum Anmeldungen vorliegen.

        Es reicht, dass ein Schüler an nur einem Tag im gesamten
        Abfragezeitraum angemeldet war, damit er erfasst wird.

        Args:
            startdatum (datetime): Erster Tag
            enddatum (datetime): Letzter Tag

        Returns:
            QuerySet: Alle Objekte im angegebenen Zeitraum, sortiert nach
                Eintritt.
        """
        return self.select_related('schueler', 'einrichtung').filter(
            (
                models.Q(eintritt__range=(startdatum, enddatum)) |
                models.Q(austritt__range=(startdatum, enddatum))
            ) | (
                models.Q(eintritt__lt=startdatum) &
                models.Q(austritt__gt=enddatum)
            )
        ).order_by('eintritt')

    def get_betreuungstage(self, startdatum, enddatum):
        """
        Gibt ein ``dictionary`` mit :model:`einrichtungen.SchuelerInEinrichtung` Objekten als Schlüssel zurück.

        Es werden nur die Objekte zurückgegeben, in denen der Schüler im
        angegebenen Zeitraum angemeldet war. Es reicht, dass der Schüler an nur
        einem Tag im gesamten Abfragezeitraum angemeldet war, damit er erfasst
        wird.

        Jeder Wert enthält einen ``tuple`` von ``date`` Objekten, die der
        Anzahl der Tage entsprechen, an denen der Schüler in der Einrichtung
        angemeldet war.

        Alle Samstage, Sonntage und Schließ­tage werden entfernt. Ob Samstage
        oder Sonntage entfernt werden, richtet sich nach der Konfiguration der
        Einrichtung.
        """
        betreuungstage = {}
        for schueler_in_einrichtung in self.zeitraum(startdatum, enddatum):
            start = schueler_in_einrichtung.eintritt
            if schueler_in_einrichtung.eintritt < startdatum:
                start = startdatum
            ende = schueler_in_einrichtung.austritt
            if schueler_in_einrichtung.austritt > enddatum:
                ende = enddatum
            betreuungstage[schueler_in_einrichtung] = tuple(
                schueler_in_einrichtung.einrichtung.get_betreuungstage(start, ende)
            )
        return betreuungstage

    def dubletten(self, schueler, eintritt, austritt):
        """Findet alle Dubletten für den Schüler im angegebenen Zeitraum."""
        return self.filter(
            schueler=schueler
        ).filter(
            (
                models.Q(eintritt__range=(eintritt, austritt)) |
                models.Q(austritt__range=(eintritt, austritt))
            ) | (
                models.Q(eintritt__lt=eintritt) &
                models.Q(austritt__gt=austritt)
            )
        )


class FerienQuerySet(models.QuerySet):

    def jahr(self, jahr):
        """Liefere alle ``Ferien`` welche im gegebenen jahr anfangen und enden."""
        return self.filter(startdatum__year=jahr, enddatum__year=jahr)


class EinrichtungHatPflegesatzQuerySet(models.QuerySet):

    def zeitraum(self, startdatum, enddatum):
        return self.filter(
            pflegesatz_startdatum__lte=startdatum, pflegesatz_enddatum__gte=enddatum
        )


class BettengeldsatzQuerySet(models.QuerySet):

    def zeitraum(self, startdatum, enddatum):
        return self.filter(startdatum__lte=startdatum, enddatum__gte=enddatum)


class BargeldsatzManager(models.Manager):

    def nach_lebensalter(self, datum, geburtsdatum):
        """
        Gibt den Bargeldsatz für das Lebensalter zurück.

        - Das Lebensalter bezieht sich immer auf das übergebene Datum
        - Nach Erreichen des 18. Lebensjahrs wird immer der Bargeldsatz für das
          18. Lebensjahr genutzt
        - Ist kein Bargeldsatz für das Lebensalter definiert, ist der
          Bargeldsatz 0 EUR

        Args:
            datum (date):
            geburtsdatum (date):

        Returns:
            Decimal: Bargeldsatz
        """
        lebensjahr = relativedelta.relativedelta(datum, geburtsdatum).years
        if lebensjahr > 18:
            lebensjahr = 18
        try:
            bargeldsatz = self.get(lebensjahr=lebensjahr)
        except self.model.DoesNotExist:
            bargeldsatz = None
        return bargeldsatz
