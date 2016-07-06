import datetime

import pytest

from absys.apps.abrechnung import services
from absys.apps.einrichtungen.models import Schliesstag


@pytest.mark.django_db
def test_get_betreuungstage_skip_weekend(betreuungstage_start, betreuungstage_ende):
    betreuungstage = services.get_betreuungstage(betreuungstage_start, betreuungstage_ende)
    assert len(betreuungstage) == 5


@pytest.mark.django_db
def test_get_betreuungstage_mit_schliesstag(betreuungstage_start, betreuungstage_ende):
    Schliesstag.objects.create(name="Test", datum=datetime.date(2016, 7, 12), art="frei")
    assert len(services.get_betreuungstage(betreuungstage_start, betreuungstage_ende)) == 4
