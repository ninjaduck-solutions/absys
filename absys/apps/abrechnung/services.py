#encoding: utf-8
from collections import namedtuple
from . import models
import datetime


#Werte = namedtuple("Werte", ["summe_aller_fehltage", "fehltage", "zahltage", "betreuungstage", "aufwendungen"])


def erstelleListeAuswahlTage(startdatum, enddatum):
    pass
    return ListeAuswahlTage

def erstelleListeAuswahlSchueler(Schueler_qs):
    pass
    return ListeAuswahlSchueler

def subtrahiereSchliesstage(ListeAuswahlTage):
    #fuer jeden Tag in ListeAuswahlTage
    pass
    return ListeAuswahlTageOhneSchliesstage

def subtrahiereWochenendtage(ListeAuswahlTageOhneSchliesstage):
    #fuer jeden Tag in ListeAuswahlTageOhneSchliesstage
    pass
    return ListeBetreuungstage

def berechneAnwesenheitAnBetreuungstag(ListeBetreuungstage, ListeAuswahlSchueler):
    #fuer jeden Tag in ListeBetreeungstage fuer jeden Schueler; hier kommen auch Fehltage rein
    pass
    return ListeAnwesenheitSchueler, Liste AbwesenheitSchueler

def zaehleAnwesenheitstage(ListeAnwesenheitSchueler):
    #Jeden Anwesenheitstag pro Schueler zaehlen
    pass
    return SummeAnwesenheitSchueler

def zaehleAbwesenheitstage(ListeAnwesenheitSchueler):
    pass
    return SummeAbwesenheitstage

def berechneSummeFehltageGesamt(SummeAbwesenheitstage):
    pass
    return SummeFehltage







def TageZurAbrechnung()








def istFerientag(datum):
    if models.Ferien.objects.filter(startdatum__lte=datum, enddatum__gte=datum):
        return 1
    else:
        return 0

def findeEinrichtungHeraus(datum, schuelerid):
     einrichtungid = models.SchuelerInEinrichtung.objects.filter(schueler_id=schuelerid, eintritt__lte=datum, austritt__gte=datum).values('einrichtung')
     return einrichtungid

#Problem: Bei Rueckgabefall 'Einrichtungspflegesatz' wird nicht das Datum herangezogen
def berechnePflegesatz(datum, schuelerid):
    einrichtungid = findeEinrichtungHeraus(datum, schuelerid)
    if istFerientag(datum) == 1:
        if models.SchuelerInEinrichtung.objects.filter \
                (schueler_id=schuelerid, einrichtung_id=einrichtungid, pers_pflegesatz_ferien=0) | \
                models.SchuelerInEinrichtung.objects.filter(schueler_id=schuelerid, einrichtung_id=einrichtungid, pers_pflegesatz_ferien_startdatum__gt=datum) | \
                models.SchuelerInEinrichtung.objects.filter(schueler_id=schuelerid, einrichtung_id=einrichtungid, pers_pflegesatz_ferien_enddatum__lt=datum):
            return models.EinrichtungHatPflegesatz.objects.filter(id=einrichtungid).values('pflegesatz_ferien')
        else:
            return models.SchuelerInEinrichtung.objects.filter(schueler_id=schuelerid, einrichtung_id=einrichtungid).values('pers_pflegesatz_ferien')
    else:
        if models.SchuelerInEinrichtung.objects.filter \
                (schueler_id=schuelerid, einrichtung_id=einrichtungid, pers_pflegesatz=0) | \
                models.SchuelerInEinrichtung.objects.filter(schueler_id=schuelerid, einrichtung_id=einrichtungid, pers_pflegesatz_startdatum__gt=datum) | \
                models.SchuelerInEinrichtung.objects.filter(schueler_id=schuelerid, einrichtung_id=einrichtungid, pers_pflegesatz_enddatum__lt=datum):
            return models.EinrichtungHatPflegesatz.objects.filter(id=einrichtungid).values('pflegesatz')
        else:
            return models.SchuelerInEinrichtung.objects.filter(schueler_id=schuelerid, einrichtung_id=einrichtungid).values('pers_pflegesatz')

# class Abrechnung(object):
#     """
#     >>> from stammdaten import services, models
#     >>> a = services.Abrechnung("2016-04-01","2016-04-30",models.Schueler.objects.all())
#     >>> a.ergebnisse
#     {<Schueler: Ränker, Martin>: Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('99.00')), <Schueler: Mueller, Kerstin>: Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('660.00'))}
#     >>> a.ergebnisse.items()
#     [(<Schueler: Ränker, Martin>, Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('99.00'))), (<Schueler: Mueller, Kerstin>, Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('660.00')))]
#     >>> a.ergebnisse.items()[0]
#     (<Schueler: Ränker, Martin>, Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('99.00')))
#     >>> a.ergebnisse.items()[0][0]
#     <Schueler: Ränker, Martin>
#     >>> a.ergebnisse.items()[0][1]
#     Werte(summe_aller_fehltage=120, fehltage=23, zahltage=33, betreuungstage=48, aufwendungen=Decimal('99.00'))
#     >>> a.ergebnisse.items()[0][1].aufwendungen
#     Decimal('99.00')
#     >>> a.ergebnisse.items()[1][1].aufwendungen
#     Decimal('660.00')
#     """

    # def __init__(self, start, ende, schueler_qs):
    #     self.ergebnisse = self._berechne(start, ende, schueler_qs)
    #     
    # def _berechne(self, start, ende, schueler_qs):
    #     ergebnisliste_schueler = {}
    #     for schueler in schueler_qs:
    #         
    #         
    #         
    #         
    #         #daten = {}
    #         #daten["summe_aller_fehltage"] = self._get_summe_aller_fehltage()
    #         #daten["fehltage"] = self._get_fehltage()
    #         #daten["zahltage"] = self._get_zahltage()
    #         #daten["betreuungstage"] = self._get_betreuungstage()
    #         #daten["aufwendungen"] = self._get_aufwendungen(schueler, ende)
    #         
    #         
    #         
    #         
    #         ergebnisliste_schueler[schueler] = Werte(**daten)
    #     return ergebnisliste_schueler
    # 
    # def _get_fehltage(self):
    #     return 23
    # 
    # def _get_zahltage(self):
    #     return 33
    # 
    # def _get_betreuungstage(self):
    #     return 48
    # 
    # def _get_summe_aller_fehltage(self):
    #     return 120
    # 
    # def _get_aufwendungen(self, schueler, ende):
    #     return self._get_zahltage() * schueler.pflegesatz(ende)
    # 