import datetime
import decimal

import pytest

from absys.apps.einrichtungen import services

context_prec_4 = decimal.Context(prec=4)
context_prec_5 = decimal.Context(prec=5)


@pytest.mark.parametrize('startdatum,enddatum,ergebnis', [
    (datetime.date(2016, 6, 1), datetime.date(2016, 6, 10), context_prec_4.create_decimal(20.22)),
    (datetime.date(2016, 6, 5), datetime.date(2016, 6, 25), context_prec_4.create_decimal(40.44)),
    (datetime.date(2016, 6, 20), datetime.date(2016, 6, 30), context_prec_4.create_decimal(20.22)),
    (datetime.date(2016, 6, 1), datetime.date(2016, 6, 30), context_prec_4.create_decimal(60.66)),
    (datetime.date(2016, 6, 1), None, context_prec_4.create_decimal(60.66)),
])
def test_bargeld_monat(startdatum, enddatum, ergebnis):
    bargeld = services.bargeld_monat(context_prec_4.create_decimal(60.66), startdatum, enddatum)
    assert bargeld == ergebnis


def test_bargeld_monat_anderer_monat():
    with pytest.raises(ValueError) as exc_info:
        services.bargeld_monat(
            decimal.Decimal(100),
            datetime.date(2016, 6, 1),
            datetime.date(2016, 7, 31)
        )
        assert str(exc_info.value) == "Start- und Enddatum müssen im gleichen Monat liegen."


def test_bargeld_monat_anderes_jahr():
    with pytest.raises(ValueError) as exc_info:
        services.bargeld_monat(
            decimal.Decimal(100),
            datetime.date(2016, 6, 1),
            datetime.date(2017, 6, 30)
        )
        assert str(exc_info.value) == "Start- und Enddatum müssen im gleichen Jahr liegen."


@pytest.mark.parametrize('startdatum,enddatum,ergebnis', [
    (datetime.date(2016, 6, 1), datetime.date(2016, 6, 10), context_prec_4.create_decimal(20.21)),
    (datetime.date(2016, 6, 5), datetime.date(2016, 6, 25), context_prec_4.create_decimal(40.43)),
    (datetime.date(2016, 6, 20), datetime.date(2016, 6, 30), context_prec_4.create_decimal(20.21)),
    (datetime.date(2016, 6, 1), datetime.date(2016, 6, 30), context_prec_4.create_decimal(60.64)),
    (datetime.date(2016, 6, 15), datetime.date(2016, 7, 31), context_prec_4.create_decimal(90.96)),
    (datetime.date(2016, 6, 1), datetime.date(2016, 8, 31), context_prec_5.create_decimal(181.92)),
    (datetime.date(2016, 6, 1), datetime.date(2016, 9, 15), context_prec_5.create_decimal(212.24)),
])
def test_bargeld_zeitraum(startdatum, enddatum, ergebnis):
    bargeld = services.bargeld_zeitraum(context_prec_4.create_decimal(60.64), startdatum, enddatum)
    assert bargeld == ergebnis
