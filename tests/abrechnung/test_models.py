import datetime

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.timezone import now


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


@pytest.mark.django_db
class TestRechnungSchueler:

    def test_nummer(self, rechnung_schueler):
        assert rechnung_schueler.nummer.endswith(str(rechnung_schueler.pk))
        assert rechnung_schueler.nummer.startswith("SR0")
        assert len(rechnung_schueler.nummer) == 8

    def test_fehltage_abrechnen_negatives_limit(self, rechnung_schueler, schueler_in_einrichtung):
        """
        Darf kein ``AssertionError: Negative indexing is not supported.`` werfen.

        Test für eine Regression bei der ``limit`` nicht auf Null oder positive
        Zahlen eingeschränkt wurde.
        """
        rechnung_schueler.fehltage_abrechnen(schueler_in_einrichtung)


@pytest.mark.django_db
class TestRechnungsPositionSchueler:

    def test_clean(self, rechnung_schueler, rechnungs_position_schueler_factory):
        with pytest.raises(IntegrityError) as exp:
            rechnungs_position_schueler_factory.build(
                datum=now(),
                rechnung_schueler=rechnung_schueler,
                rechnung_nicht_abgerechnet=rechnung_schueler
            ).clean()
        assert str(exp.value) == "Die Felder \"Schüler-Rechnung\" und \"Schüler-Rechnung, nicht abgerechnet\" dürfen nicht beide eine Schüler-Rechnung enthalten."
