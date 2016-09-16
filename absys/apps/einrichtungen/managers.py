from django.db import models


class SchuelerInEinrichtungQuerySet(models.QuerySet):

    def war_angemeldet(self, datum):
        return self.filter(
            eintritt__lte=datum,
            austritt__gte=datum
        )

    def get_betreuungstage(self, startdatum, enddatum):
        """
        Gibt ein ``dictionary`` mit :model:`einrichtungen.SchuelerInEinrichtung` Objekten als Schlüssel zurück.

        Es werden nur die Objekte zurückgegeben, in denen der Schüler im
        angegebenen Zeitraum angemeldet war. Es reicht, dass der Schüler an nur
        einem Tag im gesamten Abfragezeitraum angemeldet war, damit er erfasst
        wird.

        Jeder Wert enthält einen ``tuple`` von ``datetime`` Objekten, die der
        Anzahl der Tage entsprechen, an denen der Schüler in der Einrichtung
        angemeldet war.

        Alle Samstage, Sonntage und Schließ­tage werden entfernt.
        """
        qs = self.filter(
            (
                models.Q(eintritt__range=(startdatum, enddatum)) |
                models.Q(austritt__range=(startdatum, enddatum))
            ) | (
                models.Q(eintritt__lt=startdatum) &
                models.Q(austritt__gt=enddatum)
            )
        ).order_by('eintritt')
        betreuungstage = {}
        for schueler_in_einrichtung in qs:
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
