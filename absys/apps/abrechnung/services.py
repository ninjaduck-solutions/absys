import datetime

from absys.apps.einrichtungen.models import Schliesstag

# def erstelleListeAuswahlTage(startdatum, enddatum):
#     pass
#     return ListeAuswahlTage

# def erstelleListeAuswahlSchueler(Schueler_qs):
#     pass
#     return ListeAuswahlSchueler

# def subtrahiereSchliesstage(ListeAuswahlTage):
#     #fuer jeden Tag in ListeAuswahlTage
#     pass
#     return ListeAuswahlTageOhneSchliesstage

# def subtrahiereWochenendtage(ListeAuswahlTageOhneSchliesstage):
#     #fuer jeden Tag in ListeAuswahlTageOhneSchliesstage
#     pass
#     return ListeBetreuungstage

# def berechneAnwesenheitAnBetreuungstag(ListeBetreuungstage, ListeAuswahlSchueler):
#     #fuer jeden Tag in ListeBetreeungstage fuer jeden Schueler; hier kommen auch Fehltage rein
#     pass
#     return ListeAnwesenheitSchueler, Liste AbwesenheitSchueler

# def zaehleAnwesenheitstage(ListeAnwesenheitSchueler):
#     #Jeden Anwesenheitstag pro Schueler zaehlen
#     pass
#     return SummeAnwesenheitSchueler

# def zaehleAbwesenheitstage(ListeAnwesenheitSchueler):
#     pass
#     return SummeAbwesenheitstage

# def berechneSummeFehltageGesamt(SummeAbwesenheitstage):
#     pass
#     return SummeFehltage


def get_betreuungstage(startdatum, enddatum):
    """
    Gibt alle Tage zwischen ``startdatum`` und ``enddatum`` zurück.

    Alle Samstage, Sonntage und Schliesstage werden entfernt.
    """
    schliesstage = tuple(Schliesstag.objects.values_list('datum', flat=True))
    betreuungstage = {}
    tag = startdatum
    while tag < enddatum:
        if tag.isoweekday() not in (6, 7) and tag not in schliesstage:
            betreuungstage[tag] = ''
        tag += datetime.timedelta(1)
    return betreuungstage
