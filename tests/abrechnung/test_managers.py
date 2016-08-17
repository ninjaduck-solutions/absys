import datetime

import pytest

from absys.apps.abrechnung import models


@pytest.mark.django_db
class TestRechnungSozialamtManager:

    @pytest.mark.parametrize((
        'schueler_in_einrichtung__eintritt',
        'schueler_in_einrichtung__austritt',
        'einrichtung_hat_pflegesatz__pflegesatz_startdatum',
        'einrichtung_hat_pflegesatz__pflegesatz_enddatum',
        'anzahl'
    ), [
        (  # Anmeldung und Pflegesatz der Einrichtung entsprechen exakt dem gültigen Zeitraum
            datetime.date(2016, 6, 12),
            datetime.date(2016, 6, 17),
            datetime.date(2016, 6, 12),
            datetime.date(2016, 6, 17),
            1,
        ),
        (  # Anmeldung und Pflegesatz der Einrichtung liegen im gültigen Zeitraum
            datetime.date(2016, 6, 1),
            datetime.date(2016, 6, 30),
            datetime.date(2016, 6, 1),
            datetime.date(2016, 6, 30),
            1,
        ),
        (  # Anmeldung liegt nicht im gültigen Zeitraum
            datetime.date(2016, 5, 1),
            datetime.date(2016, 5, 31),
            datetime.date(2016, 5, 1),
            datetime.date(2016, 5, 31),
            0,
        ),
        pytest.mark.xfail(
            reason="Fehlende EinrichtungHatPflegesatz Instanz wird noch nicht behandelt")(
            (  # Pflegesatz der Einrichtung liegt nicht im gültigen Zeitraum
                datetime.date(2016, 6, 1),
                datetime.date(2016, 6, 30),
                datetime.date(2016, 5, 1),
                datetime.date(2016, 5, 31),
                0,
            )
        ),
    ])
    def test_rechnungslauf(self, sozialamt, schueler_in_einrichtung, einrichtung_hat_pflegesatz, anzahl):
        start = datetime.date(2016, 6, 12)
        ende = datetime.date(2016, 6, 17)
        assert models.RechnungSozialamt.objects.count() == 0
        assert models.Rechnung.objects.count() == 0
        models.RechnungSozialamt.objects.rechnungslauf(sozialamt, start, ende)
        assert models.RechnungSozialamt.objects.count() == 1
        assert models.Rechnung.objects.count() == anzahl
        # TODO Nachfolgende Assertions in Tests für RechnungSozialamt und Rechnung Models verschieben
        if anzahl:
            rechnung_sozialamt = models.RechnungSozialamt.objects.first()
            assert rechnung_sozialamt.sozialamt == sozialamt
            assert rechnung_sozialamt.sozialamt_anschrift == sozialamt.anschrift
            assert rechnung_sozialamt.startdatum == start
            assert rechnung_sozialamt.enddatum == ende
            assert rechnung_sozialamt.enddatum > rechnung_sozialamt.startdatum
            rechnung = models.Rechnung.objects.first()
            assert rechnung.rechnung_sozialamt == rechnung_sozialamt
            assert rechnung.schueler == schueler_in_einrichtung.schueler
            assert rechnung.name_schueler == schueler_in_einrichtung.schueler.voller_name
            assert rechnung.summe > 0
            assert rechnung.fehltage == rechnung.fehltage_gesamt == rechnung.fehltage_nicht_abgerechnet == 0
            assert rechnung.max_fehltage == schueler_in_einrichtung.fehltage_erlaubt


@pytest.mark.django_db
class TestRechnungManager:

    def test_letzte_rechnungen(self, rechnung_sozialamt_factory, rechnung_factory):
        rechnung_sozialamt_0 = rechnung_sozialamt_factory(
            startdatum=datetime.date(2015, 11, 1),
            enddatum=datetime.date(2015, 11, 30)
        )
        rechnung_factory(rechnung_sozialamt=rechnung_sozialamt_0)
        rechnung_sozialamt_1 = rechnung_sozialamt_factory(
            startdatum=datetime.date(2016, 3, 1),
            enddatum=datetime.date(2016, 3, 31)
        )
        rechnung_0 = rechnung_factory(rechnung_sozialamt=rechnung_sozialamt_1)
        rechnung_sozialamt_2 = rechnung_sozialamt_factory(
            startdatum=datetime.date(2016, 4, 1),
            enddatum=datetime.date(2016, 4, 30)
        )
        rechnung_1 = rechnung_factory(rechnung_sozialamt=rechnung_sozialamt_2)
        assert models.Rechnung.objects.letzte_rechnungen(2014).count() == 0
        assert models.Rechnung.objects.letzte_rechnungen(2015).count() == 1
        assert models.Rechnung.objects.letzte_rechnungen(2016).count() == 2
        assert models.Rechnung.objects.letzte_rechnungen(2017).count() == 0
        letzte_rechnungen = models.Rechnung.objects.letzte_rechnungen(2016)
        assert letzte_rechnungen[0] == rechnung_1
        assert letzte_rechnungen[1] == rechnung_0
