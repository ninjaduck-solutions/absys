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
        Gibt die Liste aller Tage zwischen ``startdatum`` und ``enddatum`` zurück.

        Alle Samstage, Sonntage und Schliesstage werden entfernt.
        """
        from .models import Schliesstag
        schliesstage = tuple(Schliesstag.objects.values_list('datum', flat=True))
        betreuungstage = {}
        qs = self.filter(
            models.Q(eintritt__range=(startdatum, enddatum)) |
            models.Q(austritt__range=(startdatum, enddatum)),
        ).order_by('eintritt')
        betreuungstage = {}
        for schueler_in_einrichtung in qs:
            tage = []
            tag = schueler_in_einrichtung.eintritt
            if schueler_in_einrichtung.eintritt < startdatum:
                tag = startdatum
            letzter_tag = schueler_in_einrichtung.austritt
            if schueler_in_einrichtung.austritt > enddatum:
                letzter_tag = enddatum
            while tag <= letzter_tag:
                if tag.isoweekday() not in (6, 7) and tag not in schliesstage:
                    tage.append(tag)
                tag += datetime.timedelta(1)
            betreuungstage[schueler_in_einrichtung] = tuple(tage)
        return betreuungstage
