import datetime

from django import template

register = template.Library()

@register.simple_tag
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def zeitraum_anfang_ende(zeitraum):
    """
    Liefert das Anfangs- und Enddatum eines Zeitraums.

    Zu beachten ist hier das evtl. vorhandene "Kontext" Daten *nicht*
    berücksichtigt werden da sie im Sinne unserer Definition nicht zum
    'Darstellungszeitraum' gehören.

    Returns:
        tuple: (Anfang, Ende)
    """
    def get_start(zeitraum):
        i = 0
        # Zähle die 'Kontexttage' von Beginn an.
        while zeitraum[i][1] is True:
            i += 1
        return zeitraum[i][0]

    def get_ende(zeitraum):
        i = -1
        # Zähle die 'Kontexttage' vom Ende an.
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


@register.simple_tag
def get_prefix(zeitraum, length=3):
    start = zeitraum[0] - datetime.timedelta(length)
    prefix = [start + datetime.timedelta(i) for i in range(length)]
    return prefix


@register.simple_tag
def get_suffix(zeitraum, length=3):
    end = zeitraum[-1]
    suffix = [end + datetime.timedelta(i) for i in range(1, 1 + length)]
    return suffix


@register.simple_tag
def get_prefixdaten(einrichtung_rechnung, zeitraum):
    """
    Liefer ein dict der Anwesenheiten im zeitraum für alle Schüler der Einrichtungsrechnung.

    Args:
        einrichtung_rechnung: Die ``EinrichtungRechnung`` für die die Prefixdaten erstellt werden
            sollen.
        zeitraum (tuple): Anfangs- und Endzeitraum für den das dict erstellt werden soll.

    Returns:
        dict: {Schüler: {Datum: Anwesenheit}}.
    """
    # [FIXME]
    # Statt über die die Abwesenheiten zu gehen muss hier auf evtl.
    # vorhandene Vorgängerrechnung bezug genommen werden.
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
    # Siehe ABSYS-9

    def get_anwesenheit(schueler, zeitraum):
        start = zeitraum[0]
        ende = zeitraum[-1]
        anwesenheiten = schueler.anwesenheit.filter(datum__gte=start, datum__lte=ende)
        return {anwesenheit.datum: anwesenheit.abwesend for anwesenheit in anwesenheiten}

    schueler = [position.schueler for position in einrichtung_rechnung.positionen.all()]
    return {s: get_anwesenheit(s, zeitraum) for s in schueler}

@register.simple_tag
def get_suffixdaten(einrichtung_rechnung, zeitraum):
    """
    Liefer ein dict der Anwesenheiten im zeitraum für alle Schüler der Einrichtungsrechnung.

    Args:
        einrichtung_rechnung: Die ``EinrichtungRechnung`` für die die Prefixdaten erstellt werden
            sollen.
        zeitraum (tuple): Anfangs- und Endzeitraum für den das dict erstellt werden soll.

    Returns:
        dict: {Schüler: {Datum: Anwesenheit}}.
    """
    # REVIEW
    # - Für Randtage, die nach den abgerechneten Tagen liegen, muss die
    #   Anwesenheitsliste benutzt werden. Dies ist dann aber nur eine
    #   Prognose.
    def get_anwesenheit(schueler, zeitraum):
        start = zeitraum[0]
        ende = zeitraum[-1]
        anwesenheiten = schueler.anwesenheit.filter(datum__gte=start, datum__lte=ende)
        return {anwesenheit.datum: anwesenheit.abwesend for anwesenheit in anwesenheiten}

    schueler = [position.schueler for position in einrichtung_rechnung.positionen.all()]
    return {s: get_anwesenheit(s, zeitraum) for s in schueler}
