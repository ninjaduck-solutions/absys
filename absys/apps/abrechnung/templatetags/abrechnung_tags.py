from django import template
import datetime
from django.template.defaultfilters import date as date_filter
from collections import deque, OrderedDict

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
def get_item(dictionary, key):
    return dictionary.get(key)


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
def zeitraum_anfang_ende(zeitraum):
    """
    Liefert das Anfangs- und Enddatum eines Zeitraums.abs

    Zu beachten ist hier das evtl. vorhandene "Kontext" Daten *nicht* berücksichtigt werden da
    sie im Sinne unserer Definition nicht zum 'Darstellungszeitraum' gehören.

    Returns:
        tuple: (Begin, Ende)
    """
    def get_start(zeitraum):
        i = 0
        while zeitraum[i][1] is True:
            i += 1
        return zeitraum[i][0]

    def get_ende(zeitraum):
        i = -1
        while zeitraum[i][1] is True:
            i -= 1
        return zeitraum[i][0]

    return (get_start(zeitraum), get_ende(zeitraum))


@register.filter
def ist_wochenende(datum):
    """Liefere ``True`` wenn das datum ein Wochenendstag ist."""
    return datum.weekday() in (5, 6)


@register.filter
def get_darstellungszeitraeume(rechnung):
    """
    Erzeugt relevante Datenstrukturen für die 'Zusammenfassung' einer Einrichtungsrechnung.

    Args:
        rechnung (RechnungEinrichtung): Einrichtungsrechnung die zusammengefasst werden soll.

    Returns:
        tuple: (Zeitraum, Monatsüberschriften)
    """

    def get_tage():
        """
        Liefert eine Liste von (datetime.date, bool) Tupeln.

        Jedes Tupel/Datum ist teil des relevanten Zeitraums.
        Der 'Kontext' boolean zeigt an ob es sich um einen Tag vor/nach dem eigentlichen
        Rechnungszeitraum handelt.

        Returns:
            tuple: (Datum, Kontext)
        """
        start = rechnung.rechnung_sozialamt.startdatum
        end = rechnung.rechnung_sozialamt.enddatum
        delta = end - start
        result = []
        for i in range(delta.days):
            tag = start + datetime.timedelta(i + 1)
            result.append((tag, False))
        return result

    def add_prefix(zeitraum):
        """Erweitere einen Zeitraum um 3 vorhergehende Tage."""
        offset = 3
        start = rechnung.rechnung_sozialamt.startdatum - datetime.timedelta(offset)
        prefix = [(start + datetime.timedelta(i), True) for i in range(offset)]
        zeitraum.extendleft(sorted(prefix, reverse=True))

    def add_suffix(zeitraum):
        """Erweitere einen Zeitraum um 3 nachfolgende Tage."""
        offset = 3
        end = rechnung.rechnung_sozialamt.enddatum
        suffix = [(end + datetime.timedelta(i), True) for i in range(1, 1 + offset)]
        zeitraum.extend(suffix)

    tage = get_tage()
    result = []
    while tage:
        zeitraum = deque()
        while ((len(zeitraum) < 31) and tage):
            zeitraum.append(tage.pop(0))
        result.append(zeitraum)
    add_prefix(result[0])
    add_suffix(result[-1])
    return result


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
        anwesenheiten = position.schueler.anwesenheit.filter(datum__gte=start, datum__lte=ende)

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
