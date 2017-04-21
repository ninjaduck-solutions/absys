from collections import OrderedDict

from django import template
import datetime
from django.template.defaultfilters import date as date_filter

register = template.Library()


@register.filter
def decimal_ohne_punkt(decimal, kommastellen=2):
    """
    Gibt einen Decimal ohne Punkt als Integer zurück.
    """
    return int(decimal.shift(kommastellen))


@register.filter
def integer_abgerundet(decimal, kommastellen=2):
    """
    Gibt einen Decimal als Integer zurück. Die Kommastellen
    werden werden abgeschnitten.
    """
    return int(decimal)


@register.filter
def monatsname(number):
    """
    Liefert den lokalisierten Monatsnamen anhand der Monatsnummer.

    Um die Django interne Lokalisierung zu nutzen bauen wir uns ein dummy
    ``datetime.date`` welches wir dann an den built-in ``date`` filter
    weiterreichen können.
    """
    return date_filter(datetime.date(2016, number, 1), 'F')


@register.filter
def get_schuelerdaten(rechnung):
    """
    Erstelle ein dict welches uns für jeden schüler die Tagespositionen liefert.

    Args:
        rechnung (RechnungEinrichtung): Einrichtungsrechnung die zusammengefasst werden soll.

    Returns:
        dict: {Schüler: ({Tag: Schuelerposition}, {Tag: Anwesenheit}}
    """
    def get_anwesenheit(position):
        """
        Liefere alle bekannten Anwesenheiten eines Schuelers in einem Zeitfenster.

        Der berücksichtigte Zeitraum beginnt/endet 30 Tage vor/nach dem
        Rechnungszeitraum.

        Args:
            RechnungsPositionEinrichtung: Schüler spezifische Rechnungsposten.

        Returns:
            dict: {datetime.date: bool}, wobei ``bool`` der Anwesenheitsstatus ist.
        """
        # Der Grund hierfür ist das so die Anwesenheiten für die "Kontextage"
        # zur Verfügung stehen. Dafür können wir leider nicht auf die
        # ``RechnungsPositionSchueler`` zurückgreifen. Leider erhöht dies die
        # Zahl unserer Queries beachtlich.

        start = rechnung.rechnung_sozialamt.startdatum - datetime.timedelta(days=30)
        ende = rechnung.rechnung_sozialamt.enddatum + datetime.timedelta(days=30)
        # REVIEW Warum wird 30 Tage vor und nach dem Rechnungszeitraum nach
        # Anwesenheiten gesucht? Für Randtage werden doch nur jeweils drei Tage
        # berücksichtigt. Würde es nicht ausreichen nur diese drei Tage zu
        # betrachten?
        anwesenheiten = position.schueler.anwesenheit.filter(datum__gte=start, datum__lte=ende)
        # REVIEW Hier dürfen nicht in jedem Fall die Anwesenheiten (aus
        # absys.apps.anwesenheitsliste) abgefragt werden. Die
        # Anwesenheitensdaten werden schon während des Rechnungslaufs erfasst
        # und an RechnungsPositionSchueler gespeichert. Der Grund dafür ist,
        # dass Anwesenheitensdaten im Admin geändert werden können. Die
        # Rechnungsdaten können aber nicht bearbeitet werden und bleiben so
        # konsistent. Daher dürfen in einer Rechnung nie Daten aus
        # absys.apps.anwesenheitsliste benutzt werden, wenn diese auch in
        # absys.apps.abrechnung zur Verfügung stehen. Sonst kann die
        # Darstellung inkonsistent sein, wenn die Anwesenheitensdaten
        # nachträglich verändert wurden.
        #
        # Hier muss ähnlich wie in
        # absys.apps.einrichtungen.configurations.EinrichtungKonfiguration365
        # verfahren werden:
        #
        # - Für Randtage, die vor den abgerechneten Tagen liegen, muss die
        #   vorhergehende Rechnung benutzt werden, sofern diese existiert.
        #
        # - Für Randtage, die nach den abgerechneten Tagen liegen, muss die
        #   Anwesenheitsliste benutzt werden. Dies ist dann aber nur eine
        #   Prognose.

        return {anwesenheit.datum: anwesenheit.abwesend for anwesenheit in anwesenheiten}

    def get_tagesdaten(position):
        return {sposition.datum: sposition for sposition in position.detailabrechnung}

    positionen = rechnung.positionen.all()
    return {p.schueler: (get_tagesdaten(p), get_anwesenheit(p)) for p  in positionen}


@register.filter
def monatsueberschriften(zeitraum):
    """
    Liefere ein dict für jeden relevanten Monat und die von im benötigte 'Breite'.

    Returns:
        dict: {Monatsnummer: 'Breite'}.
    """
    counter = 1
    vorheriger_tag = None
    result = OrderedDict()
    for tag, kontext in zeitraum:
        if vorheriger_tag:
            if tag.day > vorheriger_tag.day:
                counter += 1
            else:
                counter = 1
        result[tag.month] = counter
        vorheriger_tag = tag
    return result
