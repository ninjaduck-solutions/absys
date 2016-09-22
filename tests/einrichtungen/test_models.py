import datetime

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError


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

    def test_war_abwesend_keine_tage(self, schueler_in_einrichtung):
        assert schueler_in_einrichtung.war_abwesend(tuple()).count() == 0

    def test_keine_doppelte_anmeldung(self, schueler, einrichtung_factory, schueler_in_einrichtung_factory):
        """Testet, dass ein Schüler nicht zur gleichen Zeit in zwei Einrichtungen angemeldet sein kann."""
        eintritt = datetime.date(2016, 6, 1)
        austritt = datetime.date(2016, 6, 30)
        schueler_in_einrichtung_factory(
            eintritt=eintritt,
            austritt=austritt,
            schueler=schueler,
        )
        with pytest.raises(ValidationError) as exp:
            schueler_in_einrichtung = schueler_in_einrichtung_factory.build(
                eintritt=eintritt,
                austritt=austritt,
                schueler=schueler,
            )
            schueler_in_einrichtung.clean()
        assert exp.value.message.startswith("Für diesen Zeitraum existiert schon eine Anmeldung für")


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

    def test_get_betreuungstage(self, einrichtung, schliesstag_factory):
        start = datetime.date(2016, 7, 11)
        schliesstag_factory.create(
            datum=start + datetime.timedelta(3),
            einrichtungen=[einrichtung]
        )
        betreuungstage = einrichtung.get_betreuungstage(start, start + datetime.timedelta(6))
        assert len(betreuungstage) == 4
        assert betreuungstage[0] == start
        assert betreuungstage[-1] == start + datetime.timedelta(4)

    def test_get_betreuungstage_start_after_end(self, einrichtung):
        start = datetime.date(2016, 7, 11)
        betreuungstage = einrichtung.get_betreuungstage(start, start - datetime.timedelta(6))
        assert len(betreuungstage) == 0


@pytest.mark.django_db
class TestSchliesstag:

    def test_datum_unique(self, schliesstag, schliesstag_factory):
        with pytest.raises(IntegrityError):
            schliesstag_factory.create(datum=schliesstag.datum)
