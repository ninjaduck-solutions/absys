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
        return self.filter(
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

        Alle Samstage, Sonntage und Schließ­tage werden entfernt.
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
