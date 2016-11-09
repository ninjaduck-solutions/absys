import calendar
import datetime
import decimal


def bargeld_monat(bargeldanteil, startdatum, enddatum=None):
    """
    Gibt den Bargeldanteil für einen Monat zurück.
    """
    tage_monat = calendar.monthrange(startdatum.year, startdatum.month)[1]
    if enddatum is None:
        enddatum = datetime.date(startdatum.year, startdatum.month, tage_monat)
    else:
        if startdatum.month != enddatum.month:
            raise ValueError("Start- und Enddatum müssen im gleichen Monat liegen.")
        if startdatum.year != enddatum.year:
            raise ValueError("Start- und Enddatum müssen im gleichen Jahr liegen.")
    tage_anteil = enddatum.day
    if startdatum.day > 1:
        tage_anteil = enddatum.day - startdatum.day
    return bargeldanteil / tage_monat * tage_anteil


def bargeld_zeitraum(bargeldanteil, startdatum, enddatum):
    """
    Gibt den Bargeldanteil für einen Zeitraum zurück.

    Note:
        Der Zeitraum muss innerhalb eines Jahres liegen.

    Formel pro Monat:

    ::

        bargeldanteil / Tage im Monat * abgerechnete Tage in diesen Monat

    Zum Abschluss Runden auf zwei Stellen.
    """
    try:
        # Nur ein Monat
        bargeldbetrag = bargeld_monat(bargeldanteil, startdatum, enddatum)
    except ValueError:
        # Erster Monat, ab startdatum
        bargeldbetrag = bargeld_monat(bargeldanteil, startdatum)
        # Alle Monate zwischen dem ersten und letzten Monat
        monat = startdatum.month + 1
        while monat < enddatum.month:
            bargeldbetrag += bargeld_monat(
                bargeldanteil,
                datetime.date(startdatum.year, monat, 1)
            )
            monat += 1
        # Letzter Monat, bis enddatum
        bargeldbetrag += bargeld_monat(
            bargeldanteil,
            datetime.date(startdatum.year, monat, 1),
            enddatum
        )
    return bargeldbetrag.quantize(decimal.Decimal(10) ** -2)
