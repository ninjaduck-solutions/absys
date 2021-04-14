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


def get_billable_missing_days(start_date, end_date):
    def working_days_in_range(from_date, to_date):
        from_weekday = from_date.weekday()
        to_weekday = to_date.weekday()
        # If start date is after Friday, modify it to Monday
        if from_weekday > 4:
            from_weekday = 0
        day_diff = to_weekday - from_weekday
        whole_weeks = ((to_date - from_date).days - day_diff) / 7
        workdays_in_whole_weeks = whole_weeks * 5
        beginning_end_correction = min(day_diff, 5) - (max(to_weekday - 4, 0) % 5)
        working_days = workdays_in_whole_weeks + beginning_end_correction
        # Final sanity check (i.e. if the entire range is weekends)
        return max(0, working_days)

    now = datetime.datetime.now()
    if end_date.year > now.year:
        end_date = datetime.datetime(now.year, 31, 12)

    # JUST WEEKDAYS
    # open_days_total = (end_date - self.eintritt).days + 1
    open_days_total = working_days_in_range(start_date, end_date)
    billable_missing_days = decimal.Decimal(open_days_total * 0.18).quantize(
        1, rounding=decimal.ROUND_HALF_UP)
    max_number_of_billable_missing_days = 45
    return int(min(billable_missing_days, max_number_of_billable_missing_days))
