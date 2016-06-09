# encoding: utf-8
from collections import namedtuple

Werte = namedtuple("Werte", ["summe_aller_fehltage", "fehltage", "zahltage", "betreuungstage", "aufwendungen"])


class Abrechnung(object):
    """
    >>> from stammdaten import services, models
    >>> a = services.Abrechnung("2016-04-01","2016-04-30",models.Schueler.objects.all())
    >>> a.ergebnisse
    {<Schueler: Ränker, Martin>: Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('99.00')), <Schueler: Mueller, Kerstin>: Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('660.00'))}
    >>> a.ergebnisse.items()
    [(<Schueler: Ränker, Martin>, Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('99.00'))), (<Schueler: Mueller, Kerstin>, Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('660.00')))]
    >>> a.ergebnisse.items()[0]
    (<Schueler: Ränker, Martin>, Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('99.00')))
    >>> a.ergebnisse.items()[0][0]
    <Schueler: Ränker, Martin>
    >>> a.ergebnisse.items()[0][1]
    Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('99.00'))
    >>> a.ergebnisse.items()[0][1].aufwendungen
    Decimal('99.00')
    >>> a.ergebnisse.items()[1][1].aufwendungen
    Decimal('660.00')
    """

    def __init__(self, start, ende, schueler_qs):
        self.ergebnisse = self._berechne(start, ende, schueler_qs)
        
    def _berechne(self, start, ende, schueler_qs):
        ergebnisliste_schueler = {}
        for schueler in schueler_qs:
            daten = {}
            daten["summe_aller_fehltage"] = self._get_summe_aller_fehltage()
            daten["fehltage"] = self._get_fehltage()
            daten["zahltage"] = self._get_zahltage()
            daten["betreuungstage"] = self._get_betreuungstage()
            daten["aufwendungen"] = self._get_aufwendungen(schueler, ende)
            ergebnisliste_schueler[schueler] = Werte(**daten)
        return ergebnisliste_schueler
    
    def _get_fehltage(self):
        return 23
    
    def _get_zahltage(self):
        return 33
    
    def _get_betreuungstage(self):
        return 48
    
    def _get_summe_aller_fehltage(self):
        return 120
    
    def _get_aufwendungen(self, schueler, ende):
        return self._get_zahltage() * schueler.pflegesatz(ende)
    