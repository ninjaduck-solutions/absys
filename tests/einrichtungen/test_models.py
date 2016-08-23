import datetime

import pytest


@pytest.mark.django_db
class TestSchuelerInEinrichtung:

    @pytest.mark.parametrize((
        'schueler_in_einrichtung__pers_pflegesatz',
        'schueler_in_einrichtung__pers_pflegesatz_ferien',
        'schueler_in_einrichtung__pers_pflegesatz_startdatum',
        'schueler_in_einrichtung__pers_pflegesatz_enddatum',
        'ferien_daten',
        'pflegesatz',
    ), [
        (  # Persönlicher Pflegesatz ist definiert und Datum liegt im gültigen Zeitraum
            10.0,
            5.0,
            datetime.date(2016, 6, 12),
            datetime.date(2016, 6, 17),
            (datetime.date(2016, 5, 10), datetime.date(2016, 5, 17)),
            10.0,
        ),
        (  # Persönlicher Pflegesatz ist definiert und Datum liegt im gültigen Zeitraum, es sind Ferien
            10.0,
            5.0,
            datetime.date(2016, 6, 12),
            datetime.date(2016, 6, 17),
            (datetime.date(2016, 6, 10), datetime.date(2016, 6, 17)),
            5.0,
        ),
        (  # Persönlicher Pflegesatz ist definiert und Datum liegt nicht im gültigen Zeitraum
            10.0,
            5.0,
            datetime.date(2016, 5, 12),
            datetime.date(2016, 5, 17),
            (datetime.date(2016, 6, 10), datetime.date(2016, 6, 17)),
            0.0,
        ),
        (  # Persönlicher Pflegesatz ist definiert, aber Datum ist nicht definiert
            10.0,
            5.0,
            None,
            None,
            (datetime.date(2016, 6, 10), datetime.date(2016, 6, 17)),
            0.0,
        ),
    ])
    def test_get_pers_pflegesatz(self, schueler_in_einrichtung, ferien_factory, ferien_daten, pflegesatz):
        ferien_factory.create(
            startdatum=ferien_daten[0],
            enddatum=ferien_daten[1],
            einrichtungen=(schueler_in_einrichtung.einrichtung,)
        )
        datum = datetime.date(2016, 6, 15)
        assert schueler_in_einrichtung.get_pers_pflegesatz(datum) == pflegesatz

    @pytest.mark.parametrize((
        'schueler_in_einrichtung__pers_pflegesatz_startdatum',
        'schueler_in_einrichtung__pers_pflegesatz_enddatum',
    ), [
        (datetime.date(2016, 7, 12), datetime.date(2016, 7, 17))
    ])
    def test_get_pflegesatz(self, schueler_in_einrichtung):
        datum = datetime.date(2016, 7, 15)
        assert schueler_in_einrichtung.get_pflegesatz(datum) > 0.0

    def test_save(self, schueler_in_einrichtung):
        assert schueler_in_einrichtung.sozialamt == schueler_in_einrichtung.schueler.sozialamt


@pytest.mark.django_db
class TestEinrichtung:

    @pytest.mark.parametrize((
        'einrichtung_hat_pflegesatz__pflegesatz_startdatum',
        'einrichtung_hat_pflegesatz__pflegesatz_enddatum',
        'einrichtung_hat_pflegesatz__pflegesatz',
        'einrichtung_hat_pflegesatz__pflegesatz_ferien',
        'ferien_daten',
    ), [
        (  # Einrichtung hat einen Pflegesatz und Datum liegt im gültigen Zeitraum
            datetime.date(2016, 7, 12),
            datetime.date(2016, 7, 25),
            10.0,
            5.0,
            (datetime.date(2016, 5, 10), datetime.date(2016, 5, 17))
        ),
        (  # Einrichtung hat einen Pflegesatz und Datum liegt im gültigen Zeitraum, es sind Ferien
            datetime.date(2016, 7, 12),
            datetime.date(2016, 7, 25),
            5.0,
            10.0,
            (datetime.date(2016, 7, 10), datetime.date(2016, 7, 17))
        ),
    ])
    def test_get_pflegesatz_success(self, einrichtung_hat_pflegesatz, ferien_factory, ferien_daten):
        ferien_factory.create(
            startdatum=ferien_daten[0],
            enddatum=ferien_daten[1],
            einrichtungen=(einrichtung_hat_pflegesatz.einrichtung,)
        )
        datum = datetime.date(2016, 7, 15)
        assert einrichtung_hat_pflegesatz.einrichtung.get_pflegesatz(datum) == 10.0

    @pytest.mark.parametrize((
        'einrichtung_hat_pflegesatz__pflegesatz_startdatum',
        'einrichtung_hat_pflegesatz__pflegesatz_enddatum',
    ), [
        (datetime.date(2015, 7, 12), datetime.date(2015, 7, 25)),
    ])
    def test_get_pflegesatz_failure(self, einrichtung_hat_pflegesatz):
        datum = datetime.date(2016, 7, 15)
        with pytest.raises(einrichtung_hat_pflegesatz.DoesNotExist):
            einrichtung_hat_pflegesatz.einrichtung.get_pflegesatz(datum)
