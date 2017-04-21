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
    for tag, kontext in zeitraum:
        if vorheriger_tag:
            if tag.day > vorheriger_tag.day:
                counter += 1
            else:
                counter = 1
        result[tag.month] = counter
        vorheriger_tag = tag
    return result
