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
        for i in range(delta.days + 1):
            tag = start + datetime.timedelta(i)
            result.append((tag, False))
        return result
        # REVIEW Wir benutzen arrow schon in den Tests. Wenn arrow in die
        # setup.py eingetragen werden würde, könnte es auch hier benutzt
        # werden:
        #
        # tage = arrow.Arrow.range(
        #     'day',
        #     arrow.get(rechnung.rechnung_sozialamt.startdatum),
        #     arrow.get(rechnung.rechnung_sozialamt.enddatum)
        # )
        # return list(zip([t.date() for t in tage], [False] * len(tage)))
        #
        # Natürlich liefern beide Möglichkeiten das gleiche Ergebnis. IMHO ist
        # die Lesbarkeit mit arrow besser, vor allem bei den beiden folgenden
        # Beispielen, die replace() nutzen.

    def add_prefix(zeitraum):
        """Erweitere einen Zeitraum um 3 vorhergehende Tage."""
        offset = 3
        start = rechnung.rechnung_sozialamt.startdatum - datetime.timedelta(offset)
        prefix = [(start + datetime.timedelta(i), True) for i in range(offset)]
        zeitraum.extendleft(sorted(prefix, reverse=True))
        # REVIEW Hier könnte auch arrow genutzt werden:
        #
        # tage = arrow.Arrow.range(
        #     'day',
        #     arrow.get(rechnung.rechnung_sozialamt.startdatum).replace(days=-3),
        #     limit=3
        # )
        # zeitraum.extendleft(zip(reversed([t.date() for t in tage]), [True] * len(tage)))

    def add_suffix(zeitraum):
        """Erweitere einen Zeitraum um 3 nachfolgende Tage."""
        offset = 3
        end = rechnung.rechnung_sozialamt.enddatum
        suffix = [(end + datetime.timedelta(i), True) for i in range(1, 1 + offset)]
        zeitraum.extend(suffix)
        # REVIEW Hier könnte auch arrow genutzt werden:
        #
        # tage = arrow.Arrow.range(
        #     'day',
        #     arrow.get(rechnung.rechnung_sozialamt.enddatum).replace(days=+1),
        #     limit=3
        # )
        # zeitraum.extend(zip([t.date() for t in tage]), [True] * len(tage))

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
