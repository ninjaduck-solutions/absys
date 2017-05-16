import datetime

from django import template

register = template.Library()

@register.simple_tag
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def zusammenfassung_klasse(datum, kontext=None, vermindert=None):
    """
    Liefere die passende Klasse für ein gegebenes Datum.

    Das wir eine Tag nehmen hat den Vorteil das die Logik und die Klassen-
    namen nur einmal zentral bestimmt werden müssen.
    """
    def ist_wochenende(datum):
        return datum.weekday() in (5, 6)

    if kontext:
        result = 'zeitraum-kontext'
    elif vermindert:
        result = 'vermindert'
    elif ist_wochenende(datum):
        result = 'weekend'
    else:
        result = ''

    return result


@register.simple_tag
def get_prefixdaten(einrichtung_rechnung, zeitraum):
    """
    Liefere die Schülerdaten für den Prefixzeitraum. Für Details siehe die Modelmethode.

    Dies ist notwendig um den Zeitraum an die Model-Methode übergeben zu können.

    Durch diese Lösung stellen wir sicher das die Logik *am* Model ist und gleichzeitig flexibel
    genug um mit verschiedenen Zeiträumen zu arbeiten.
    """
    return einrichtung_rechnung.get_prefixdaten(zeitraum)


@register.simple_tag
def get_suffixdaten(einrichtung_rechnung, zeitraum):
    """
    Liefere die Schülerdaten für den Suffixzeitraum. Für Details siehe die Modelmethode.

    Dies ist notwendig um den Zeitraum an die Model-Methode übergeben zu können.

    Durch diese Lösung stellen wir sicher das die Logik *am* Model ist und gleichzeitig flexibel
    genug um mit verschiedenen Zeiträumen zu arbeiten.
    """
    return einrichtung_rechnung.get_suffixdaten(zeitraum)
