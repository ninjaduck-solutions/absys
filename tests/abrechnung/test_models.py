import datetime

import pytest
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from absys.apps.abrechnung import models


@pytest.mark.django_db
class TestRechnungSozialamt:

    def test_nummer(self, rechnung_sozialamt):
        assert rechnung_sozialamt.nummer.endswith(str(rechnung_sozialamt.pk))
        assert rechnung_sozialamt.nummer.startswith("S0")
        assert len(rechnung_sozialamt.nummer) == 7

    def test_clean(self, rechnung_sozialamt_factory):
        rechnung_sozialamt_factory.build().clean()

    @pytest.mark.parametrize(('startdatum_timedelta', 'enddatum_timedelta'), [
        (0, 0), (5, 5), (-5, -5), (-5, 5), (5, -5)
    ])
    def test_clean_duplicate(self, rechnung_sozialamt, rechnung_sozialamt_factory, startdatum_timedelta,
            enddatum_timedelta):
        with pytest.raises(ValidationError):
            rechnung_sozialamt_factory.build(
                sozialamt=rechnung_sozialamt.sozialamt,
                startdatum=rechnung_sozialamt.startdatum + datetime.timedelta(startdatum_timedelta),
                enddatum=rechnung_sozialamt.enddatum + datetime.timedelta(enddatum_timedelta)
            ).clean()

    def test_clean_start_nicht_nach_ende(self, rechnung_sozialamt_factory):
        """Testet, dass ein ``ValidationError`` geworfen wird, wenn startdatum nach enddatum liegt."""
        rechnung_sozialamt = rechnung_sozialamt_factory.build(zeitraum=-2)
        with pytest.raises(ValidationError):
            rechnung_sozialamt.clean()

    def test_clean_start_ende_nicht_gleiches_jahr(self, rechnung_sozialamt_factory):
        """Testet, dass ein ``ValidationError`` geworfen wird, wenn startdatum und enddatum nicht im gleichen Jahr liegen."""
        rechnung_sozialamt = rechnung_sozialamt_factory.build(zeitraum=400)
        with pytest.raises(ValidationError):
            rechnung_sozialamt.clean()

    def test_clean_ende_groesser_heute(self, rechnung_sozialamt_factory):
        """Testet, dass ein ``ValidationError`` geworfen wird, wenn enddatum nach "Heute" liegt."""
        rechnung_sozialamt = rechnung_sozialamt_factory.build()
        rechnung_sozialamt.startdatum = now().date()
        rechnung_sozialamt.enddatum = now().date() + datetime.timedelta(1)
        with pytest.raises(ValidationError):
            rechnung_sozialamt.clean()

    def test_fehltage_abrechnen_negatives_limit(self, rechnung_sozialamt, schueler_in_einrichtung):
        """
        Darf kein ``AssertionError: Negative indexing is not supported.`` werfen.

        Test für eine Regression bei der ``limit`` nicht auf Null oder positive
        Zahlen eingeschränkt wurde.
        """
        rechnung_sozialamt.fehltage_abrechnen(schueler_in_einrichtung)

    def test_delete(self, rechnung_sozialamt_factory, sozialamt_factory):
        sozialamt_2 = sozialamt_factory()
        first = rechnung_sozialamt_factory(enddatum=datetime.date(2016, 1, 31))
        obj = rechnung_sozialamt_factory(enddatum=datetime.date(2016, 2, 29))
        rechnung_sozialamt_factory(enddatum=datetime.date(2016, 3, 31))
        rechnung_sozialamt_factory(enddatum=datetime.date(2016, 3, 31), sozialamt=sozialamt_2)
        rechnung_sozialamt_factory(enddatum=datetime.date(2016, 4, 30), sozialamt=sozialamt_2)
        rechnung_sozialamt_factory(enddatum=datetime.date(2016, 4, 30))
        last = rechnung_sozialamt_factory(enddatum=datetime.date(2017, 1, 31))
        assert models.RechnungSozialamt.objects.count() == 7
        obj.delete()
        assert models.RechnungSozialamt.objects.count() == 2
        assert models.RechnungSozialamt.objects.get(pk=first.pk)
        assert models.RechnungSozialamt.objects.get(pk=last.pk)


@pytest.mark.django_db
class TestRechnungsPositionEinrichtung:

    def test_detailabrechnung(self, schueler, rechnung_sozialamt_factory,
            einrichtung_hat_pflegesatz_factory, schueler_in_einrichtung_factory):
        rechnung_sozialamt_factory(enddatum=datetime.date(2016, 5, 31))
        pflegesatz_start = datetime.date(2016, 1, 1)
        start = datetime.date(2016, 6, 1)
        ende = datetime.date(2016, 6, 30)
        schueler_in_einrichtung_1 = schueler_in_einrichtung_factory(
            schueler=schueler,
            eintritt=start,
            tage_angemeldet=14
        )
        einrichtung_hat_pflegesatz_factory(
            einrichtung=schueler_in_einrichtung_1.einrichtung,
            pflegesatz_startdatum=pflegesatz_start,
            pflegesatz_dauer=(ende - pflegesatz_start).days
        )
        schueler_in_einrichtung_2 = schueler_in_einrichtung_factory(
            schueler=schueler,
            eintritt=start + datetime.timedelta(15),
            tage_angemeldet=14
        )
        einrichtung_hat_pflegesatz_factory(
            einrichtung=schueler_in_einrichtung_2.einrichtung,
            pflegesatz_startdatum=pflegesatz_start,
            pflegesatz_dauer=(ende - pflegesatz_start).days
        )
        assert schueler_in_einrichtung_1.einrichtung != schueler_in_einrichtung_2.einrichtung
        rechnung_sozialamt = models.RechnungSozialamt.objects.rechnungslauf(schueler.sozialamt, ende)
        assert rechnung_sozialamt.rechnungen_einrichtungen.count() == 2
        assert schueler.positionen_schueler.count() == 22
        for rechnung_einrichtung in rechnung_sozialamt.rechnungen_einrichtungen.all():
            assert rechnung_einrichtung.positionen.filter(schueler=schueler).count() == 1
            pos = rechnung_einrichtung.positionen.filter(schueler=schueler).first()
            assert pos.detailabrechnung.count() == 11
