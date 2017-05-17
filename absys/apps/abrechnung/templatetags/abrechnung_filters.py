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
def monatsueberschriften(zeitraum):
    """
    Liefere ein dict für jeden relevanten Monat und die von im benötigte 'Breite'.

    Returns:
        dict: {Monatsnummer: 'Breite'}.
    """
    counter = 1
    vorheriger_tag = None
    result = OrderedDict()
    for tag in zeitraum:
        if vorheriger_tag:
            if tag.day > vorheriger_tag.day:
                counter += 1
            else:
                counter = 1
        result[tag.month] = counter
        vorheriger_tag = tag
    return result


@register.filter
def zusammenfassung_anwesenheitssymbol(position, daten):
    """Rendere das passende Zeichen zur Darstellung der Anwesenheit eines Schülers."""
    def ist_anfahrt(datum, daten):
        """Liefere ``True`` wenn das Datum davor 'abwesend' war."""
        result = False
        vortag = datum - datetime.timedelta(1)
        vortag_daten = daten.get(vortag)
        # Es ist nicht garantiert das für den Vortag überhaupt eine Position
        # vorliegt.
        if vortag_daten:
            result = vortag_daten.abwesend
        return result

    def ist_abfahrt(datum, daten):
        """Liefere ``True`` wenn das Datum danach 'abwesend' war."""
        result = False
        folgetag = datum + datetime.timedelta(1)
        folgetag_daten = daten.get(folgetag)
        # Es ist nicht garantiert das für den Folgetag überhaupt eine Position
        # vorliegt.
        if folgetag_daten:
            result = folgetag_daten.abwesend
        return result

    if position:
        if position.abwesend:
            result = 'H'
        else:
            if ist_anfahrt(position.datum, daten) or ist_abfahrt(position.datum, daten):
                result = 'A'
            else:
                result = '1'
    else:
        result = '--'
    return result


@register.filter
def zusammenfassung_kontext_anwesenheitssymbol(anwesenheit):
    if anwesenheit is None:
        result = '--'
    elif anwesenheit is False:
        result = 'H'
    else:
        result = '1'
    return result
