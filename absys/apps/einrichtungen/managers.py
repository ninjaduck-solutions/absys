import datetime

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
        from .models import Schliesstag
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
        schliesstage = {}
        for schueler_in_einrichtung in qs:
            einrichtung = schueler_in_einrichtung.einrichtung
            if einrichtung not in schliesstage:
                schliesstage[einrichtung] = tuple(
                    Schliesstag.objects.filter(einrichtungen__in=[einrichtung]).values_list('datum', flat=True)
                )
            tage = []
            tag = schueler_in_einrichtung.eintritt
            if schueler_in_einrichtung.eintritt < startdatum:
                tag = startdatum
            letzter_tag = schueler_in_einrichtung.austritt
            if schueler_in_einrichtung.austritt > enddatum:
                letzter_tag = enddatum
            while tag <= letzter_tag:
                if tag.isoweekday() not in (6, 7) and tag not in schliesstage[einrichtung]:
                    tage.append(tag)
                tag += datetime.timedelta(1)
            betreuungstage[schueler_in_einrichtung] = tuple(tage)
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
