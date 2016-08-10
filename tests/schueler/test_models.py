import datetime

import pytest


@pytest.mark.django_db
class TestSchueler:

    @pytest.mark.parametrize((
        'schueler_in_einrichtung__pers_pflegesatz',
        'schueler_in_einrichtung__pers_pflegesatz_startdatum',
        'schueler_in_einrichtung__pers_pflegesatz_enddatum',
        'schueler_in_einrichtung__eintritt',
        'schueler_in_einrichtung__austritt',
        'ergebnis',
    ), [
        (  # Datum für persönlichen Pflegesatz liegt im gültigen Zeitraum, Schüler war angemeldet
            10.0,
            datetime.date(2016, 7, 11),
            datetime.date(2016, 7, 15),
            datetime.date(2016, 7, 12),
            datetime.date(2016, 7, 25),
            10.0,
        ),
        (  # Datum für persönlichen Pflegesatz liegt nicht im gültigen Zeitraum, Schüler war nicht angemeldet
            10.0,
            datetime.date(2016, 5, 11),
            datetime.date(2016, 5, 15),
            datetime.date(2016, 5, 12),
            datetime.date(2016, 5, 25),
            0.0,
        ),
    ])
    def test_berechne_pflegesatz(self, schueler, schueler_in_einrichtung, ergebnis):
        datum = datetime.date(2016, 7, 12)
        assert schueler.berechne_pflegesatz(datum) == ergebnis
        if ergebnis == 0.0:
            with pytest.raises(schueler_in_einrichtung.DoesNotExist):
                schueler.angemeldet_in_einrichtung.war_angemeldet(datum).get()
