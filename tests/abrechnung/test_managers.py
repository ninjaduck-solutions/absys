import datetime

import pytest

from absys.apps.abrechnung import models


@pytest.mark.django_db
class TestRechnungManager:

    @pytest.mark.parametrize((
        'schueler_in_einrichtung__eintritt',
        'schueler_in_einrichtung__austritt',
        'einrichtung_hat_pflegesatz__pflegesatz_startdatum',
        'einrichtung_hat_pflegesatz__pflegesatz_enddatum',
        'anzahl'
    ), [
        (  # Anmeldung und Pflegesatz der Einrichtung liegen im gültigen Zeitraum
            datetime.date(2016, 6, 12),
            datetime.date(2016, 6, 17),
            datetime.date(2016, 6, 12),
            datetime.date(2016, 6, 17),
            1,
        ),
        (  # Anmeldung liegt nicht im gültigen Zeitraum
            datetime.date(2016, 5, 12),
            datetime.date(2016, 5, 17),
            datetime.date(2016, 6, 12),
            datetime.date(2016, 6, 17),
            0,
        ),
        pytest.mark.xfail(
            reason="Fehlende EinrichtungHatPflegesatz Instanz wird noch nicht behandelt")(
            (  # Pflegesatz der Einrichtung liegt nicht im gültigen Zeitraum
                datetime.date(2016, 6, 12),
                datetime.date(2016, 6, 17),
                datetime.date(2016, 5, 12),
                datetime.date(2016, 5, 17),
                0,
            )
        ),
    ])
    def test_rechnungslauf(self, sozialamt, schueler_in_einrichtung, einrichtung_hat_pflegesatz, anzahl):
        start = datetime.date(2016, 6, 12)
        ende = datetime.date(2016, 6, 17)
        assert models.Rechnung.objects.count() == 0
        models.Rechnung.objects.rechnungslauf(sozialamt, start, ende)
        assert models.Rechnung.objects.count() == anzahl
        # TODO Nachfolgende Assertions in Tests für Rechnung Model verschieben
        if anzahl:
            rechnung = models.Rechnung.objects.first()
            assert rechnung.sozialamt == sozialamt
            assert rechnung.schueler == schueler_in_einrichtung.schueler
            assert rechnung.startdatum == start
            assert rechnung.enddatum == ende
            assert rechnung.enddatum > rechnung.startdatum
            assert rechnung.name_schueler == schueler_in_einrichtung.schueler.voller_name
            assert rechnung.summe > 0
            assert rechnung.fehltage == rechnung.fehltage_gesamt == rechnung.fehltage_nicht_abgerechnet == 0
            assert rechnung.max_fehltage == schueler_in_einrichtung.fehltage_erlaubt
