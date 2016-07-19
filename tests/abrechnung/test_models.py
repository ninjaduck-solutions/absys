import datetime

import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestRechnung:

    def test_nummer(self, rechnung):
        assert rechnung.nummer.endswith(str(rechnung.pk))
        assert rechnung.nummer.startswith("0")
        assert len(rechnung.nummer) == 6

    def test_clean(self, rechnung_factory):
        rechnung_factory.build().clean()

    @pytest.mark.parametrize(('startdatum_timedelta', 'enddatum_timedelta'), [
        (0, 0), (5, 5), (-5, -5), (-5, 5), (5, -5)
    ])
    def test_clean_duplicate(self, rechnung, rechnung_factory, startdatum_timedelta,
            enddatum_timedelta):
        with pytest.raises(ValidationError):
            rechnung_factory.build(
                sozialamt=rechnung.sozialamt,
                schueler=rechnung.schueler,
                startdatum=rechnung.startdatum + datetime.timedelta(startdatum_timedelta),
                enddatum=rechnung.enddatum + datetime.timedelta(enddatum_timedelta)
            ).clean()

    def test_clean_start_ende(self, rechnung_factory):
        rechnung = rechnung_factory.build()
        rechnung.startdatum = rechnung.enddatum + datetime.timedelta(2)
        with pytest.raises(ValidationError):
            rechnung.clean()
