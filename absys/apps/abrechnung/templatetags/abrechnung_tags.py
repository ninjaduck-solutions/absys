from django import template

register = template.Library()

@register.simple_tag
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def zeitraum_anfang_ende(zeitraum):
    """
    Liefert das Anfangs- und Enddatum eines Zeitraums.

    Zu beachten ist hier das evtl. vorhandene "Kontext" Daten *nicht* berücksichtigt werden da
    sie im Sinne unserer Definition nicht zum 'Darstellungszeitraum' gehören.

    Returns:
        tuple: (Anfang, Ende)
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
