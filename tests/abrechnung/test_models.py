import datetime

import pytest
from django.core.exceptions import ValidationError
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
class TestRechnung:

    def test_nummer(self, rechnung):
        assert rechnung.nummer.endswith(str(rechnung.pk))
        assert rechnung.nummer.startswith("R0")
        assert len(rechnung.nummer) == 7
