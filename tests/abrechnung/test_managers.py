import datetime

import pytest
from django.utils import timezone

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
    def test_rechnungslauf(self, sozialamt, schueler_in_einrichtung, einrichtung_hat_pflegesatz,
            anwesenheit_factory, buchungskennzeichen, anzahl):
        start = datetime.date(2016, 6, 12)
        ende = datetime.date(2016, 6, 17)
        anwesenheit_factory.create(
            schueler=schueler_in_einrichtung.schueler,
            einrichtung=schueler_in_einrichtung.einrichtung,
            datum=ende,
            abwesend=True
        )
        assert models.RechnungSozialamt.objects.count() == 0
        assert models.RechnungEinrichtung.objects.count() == 0
        models.RechnungSozialamt.objects.rechnungslauf(sozialamt, start, ende)
        assert models.RechnungSozialamt.objects.count() == 1
        assert models.RechnungEinrichtung.objects.count() == anzahl
        # TODO Nachfolgende Assertions in Tests der entsprechenden Models verschieben
        if anzahl:
            # RechnungSozialamt
            rechnung_sozialamt = models.RechnungSozialamt.objects.first()
            assert rechnung_sozialamt.sozialamt == sozialamt
            assert rechnung_sozialamt.sozialamt_anschrift == sozialamt.anschrift
            assert rechnung_sozialamt.startdatum == start
            assert rechnung_sozialamt.enddatum == ende
            assert rechnung_sozialamt.enddatum > rechnung_sozialamt.startdatum
            assert rechnung_sozialamt.positionen_schueler.count() == 5
            pos_schueler = rechnung_sozialamt.positionen_schueler.first()
            # RechnungsPositionSchueler
            assert pos_schueler.rechnung_sozialamt == rechnung_sozialamt
            assert pos_schueler.schueler == schueler_in_einrichtung.schueler
            assert pos_schueler.einrichtung == schueler_in_einrichtung.einrichtung
            assert pos_schueler.datum == start + datetime.timedelta(1)
            assert pos_schueler.abgerechnet
            assert pos_schueler.name_schueler == schueler_in_einrichtung.schueler.voller_name
            assert pos_schueler.name_einrichtung == schueler_in_einrichtung.einrichtung.name
            assert pos_schueler.abwesend is False
            assert pos_schueler.pflegesatz > 0
            assert rechnung_sozialamt.positionen_schueler.last().datum == ende
            # RechnungEinrichtung
            rechnung = models.RechnungEinrichtung.objects.first()
            assert rechnung.rechnung_sozialamt == rechnung_sozialamt
            assert rechnung.einrichtung == schueler_in_einrichtung.einrichtung
            assert rechnung.name_einrichtung == schueler_in_einrichtung.einrichtung.name
            assert len(rechnung.buchungskennzeichen) > 0
            assert rechnung.datum_faellig > timezone.now().date()
            assert rechnung.betreuungstage == 5
            assert rechnung.summe > 0
            assert rechnung.positionen.count() == 1
            # RechnungsPositionEinrichtung
            pos_einrichtung = rechnung.positionen.first()
            assert pos_einrichtung.fehltage_max > 0
            assert pos_einrichtung.anwesend == 5
            assert pos_einrichtung.fehltage == 0
            assert pos_einrichtung.fehltage_uebertrag == 0
            assert pos_einrichtung.fehltage_gesamt == (
                pos_einrichtung.fehltage + pos_einrichtung.fehltage_uebertrag
            )
            assert pos_einrichtung.fehltage_abrechnung == 0
            assert pos_einrichtung.zahltage == 5
            assert pos_einrichtung.detailabrechnung.count() == 5
