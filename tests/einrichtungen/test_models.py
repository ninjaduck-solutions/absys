import datetime

import pytest

from absys.apps.einrichtungen.models import Schliesstag, SchuelerInEinrichtung


@pytest.mark.django_db
def test_get_betreuungstage_skip_weekend(betreuungstage_start, betreuungstage_ende):
    betreuungstage = SchuelerInEinrichtung.get_betreuungstage(betreuungstage_start, betreuungstage_ende)
    assert len(betreuungstage) == 5
    assert betreuungstage[0] is betreuungstage_start


@pytest.mark.django_db
def test_get_betreuungstage_mit_schliesstag(betreuungstage_start, betreuungstage_ende):
    Schliesstag.objects.create(name="Test", datum=datetime.date(2016, 7, 12), art="frei")
    assert len(SchuelerInEinrichtung.get_betreuungstage(betreuungstage_start, betreuungstage_ende)) == 4
