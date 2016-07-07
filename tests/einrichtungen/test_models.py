import datetime

import pytest

from absys.apps.einrichtungen.models import SchuelerInEinrichtung


@pytest.mark.parametrize(('schliesstag__datum, count'), [
    (datetime.date(2016, 7, 12), 4),
    (datetime.date(2015, 7, 12), 5),
])
@pytest.mark.django_db
def test_get_betreuungstage(betreuungstage_start, betreuungstage_ende, schliesstag, count):
    betreuungstage = SchuelerInEinrichtung.get_betreuungstage(betreuungstage_start, betreuungstage_ende)
    assert len(betreuungstage) == count
    assert betreuungstage[0] is betreuungstage_start
