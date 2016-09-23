import datetime

import arrow
import pytest
from django.utils import timezone
from freezegun import freeze_time

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
            anwesenheit_factory, buchungskennzeichen, anzahl, rechnung_sozialamt_factory):
        rechnung_sozialamt_factory(sozialamt=sozialamt, enddatum=datetime.date(2016, 6, 11))
        start = datetime.date(2016, 6, 12)
        ende = datetime.date(2016, 6, 17)
        anwesenheit_factory(
            schueler=schueler_in_einrichtung.schueler,
            einrichtung=schueler_in_einrichtung.einrichtung,
            datum=ende,
            abwesend=True
        )
        assert models.RechnungSozialamt.objects.count() == 1
        assert models.RechnungEinrichtung.objects.count() == 0
        rechnung_sozialamt = models.RechnungSozialamt.objects.rechnungslauf(sozialamt, ende)
        assert models.RechnungSozialamt.objects.count() == 2
        assert models.RechnungEinrichtung.objects.count() == anzahl
        # TODO Nachfolgende Assertions in Tests der entsprechenden Models verschieben
        if anzahl:
            # RechnungSozialamt
            assert rechnung_sozialamt.sozialamt == sozialamt
            assert rechnung_sozialamt.name_sozialamt == sozialamt.name
            assert rechnung_sozialamt.anschrift_sozialamt == sozialamt.anschrift
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
            assert pos_einrichtung.fehltage_max == schueler_in_einrichtung.fehltage_erlaubt > 0
            assert pos_einrichtung.anwesend == 4
            assert pos_einrichtung.fehltage == 1
            assert pos_einrichtung.fehltage_uebertrag == 0
            assert pos_einrichtung.fehltage_gesamt == (
                pos_einrichtung.fehltage + pos_einrichtung.fehltage_uebertrag
            )
            assert pos_einrichtung.fehltage_abrechnung == 1
            assert pos_einrichtung.zahltage == 5
            assert pos_einrichtung.detailabrechnung.count() == 5

    @pytest.mark.slowtest
    def test_get_startdatum(self, sozialamt):
        """
        Testet, dass das Startdatum der 1.1. im Jahr des Enddatums ist.
        """
        start = datetime.datetime(2015, 1, 1, 0, 0, 0)
        end = datetime.datetime(2016, 12, 31, 0, 0, 0)
        for date in arrow.Arrow.range('day', start, end):
            print(date)
            with freeze_time(date.format('YYYY-MM-DD')):
                enddatum = timezone.now().date()
                startdatum = models.RechnungSozialamt.objects.get_startdatum(sozialamt, enddatum)
                assert startdatum == datetime.date(enddatum.year, 1, 1)

    def test_get_startdatum_rechnung_danach(self, sozialamt, rechnung_sozialamt_factory):
        """
        Testet, dass das Startdatum der 1.1. im Jahr des Enddatums ist.

        Obwohl schon eine Rechnung in einem späteren Jahr existiert, liegt das
        Startdatum im Jahr des Enddatums.
        """
        start = datetime.datetime(2015, 1, 1, 0, 0, 0)
        end = datetime.datetime(2016, 12, 31, 0, 0, 0)
        for date in arrow.Arrow.range('day', start, end):
            print(date)
            with freeze_time(date.format('YYYY-MM-DD')):
                if timezone.now().date() == datetime.date(2016, 1, 2):
                    continue
                rechnung = rechnung_sozialamt_factory(sozialamt=sozialamt, enddatum=timezone.now().date())
                enddatum = rechnung.enddatum - datetime.timedelta(366)
                startdatum = models.RechnungSozialamt.objects.get_startdatum(sozialamt, enddatum)
                assert startdatum < rechnung.startdatum
                assert startdatum.year == enddatum.year
                assert startdatum.month == 1
                assert startdatum.day == 1

    @freeze_time('2016-03-01')
    def test_get_startdatum_rechnung_davor_gleiches_jahr(self, sozialamt, rechnung_sozialamt_factory):
        """
        Testet, dass das Startdatum einen Tag nach dem Enddatum der vorherigen Rechnung liegt.

        Die vorherige Rechnung liegt im gleichen Jahr.
        """
        enddatum = timezone.now().date() - datetime.timedelta(1)
        rechnung = rechnung_sozialamt_factory(sozialamt=sozialamt, enddatum=enddatum)
        enddatum = timezone.now().date() + datetime.timedelta(30)
        startdatum = models.RechnungSozialamt.objects.get_startdatum(sozialamt, enddatum)
        assert startdatum == rechnung.enddatum + datetime.timedelta(1)

    def test_get_startdatum_rechnung_davor_anderes_jahr(self, sozialamt, rechnung_sozialamt_factory):
        """
        Testet, dass das Startdatum am 1.1. des Jahres des Enddatums liegt.

        Es existiert eine vorherige Rechnung im vorherigen Jahr, diese wird
        aber nicht in Betracht gezogen.
        """
        with freeze_time('2015-10-31'):
            enddatum = timezone.now().date()
            rechnung = rechnung_sozialamt_factory(sozialamt=sozialamt, enddatum=enddatum)
        with freeze_time('2016-05-31'):
            enddatum = timezone.now().date()
            startdatum = models.RechnungSozialamt.objects.get_startdatum(sozialamt, enddatum)
        assert startdatum > rechnung.enddatum
        assert startdatum.year == 2016
        assert startdatum.month == 1
        assert startdatum.day == 1
