import datetime

import pytest

from absys.apps.einrichtungen.models import SchuelerInEinrichtung


@pytest.mark.django_db
class TestSchuelerInEinrichtungQuerySet:

    @pytest.mark.parametrize((
        'schliesstag__datum',
        'schueler_in_einrichtung__eintritt',
        'schueler_in_einrichtung__austritt',
        'count'
    ), [
        (  # Eintritt vor Start, Austritt nach Ende, ein Schliesstag
            datetime.date(2016, 7, 12),
            datetime.date(2016, 7, 8),
            datetime.date(2016, 7, 18),
            4
        ),
        (  # Eintritt vor Start, Austritt nach Ende, kein Schliesstag
            datetime.date(2015, 7, 12),
            datetime.date(2016, 7, 8),
            datetime.date(2016, 7, 18),
            5
        ),
        (  # Schueler im Zeitraum nicht in Einrichtung
            datetime.date(2015, 7, 12),
            datetime.date(2015, 7, 8),
            datetime.date(2015, 7, 18),
            0
        ),
    ])
    def test_get_betreuungstage(
            self, schueler, betreuungstage_start, betreuungstage_ende, schliesstag,
            schueler_in_einrichtung, count):
        betreuungstage = schueler.angemeldet_in_einrichtung.get_betreuungstage(
            betreuungstage_start,
            betreuungstage_ende
        )
        for schueler_in_einrichtung, tage in betreuungstage.items():
            assert isinstance(schueler_in_einrichtung, SchuelerInEinrichtung)
            assert len(tage) == count
            assert tage[0] is betreuungstage_start

    @pytest.mark.parametrize((
        'schueler_in_einrichtung__eintritt',
        'schueler_in_einrichtung__austritt',
    ), [
        (
            datetime.date(2016, 7, 7),
            datetime.date(2016, 7, 13),
        ),
    ])
    def test_get_betreuungstage_zwei_einrichtungen(
            self, schueler, schueler_factory, betreuungstage_start, betreuungstage_ende,
            schliesstag_factory, schueler_in_einrichtung, schueler_in_einrichtung_factory,
            einrichtung_factory):
        schliesstag_factory(datum=datetime.date(2016, 7, 12))
        schliesstag_factory(datum=datetime.date(2016, 7, 14))
        schueler_in_einrichtung_2 = schueler_in_einrichtung_factory(
            schueler=schueler,
            einrichtung=einrichtung_factory(),
            eintritt=datetime.date(2016, 7, 14),
            austritt=datetime.date(2016, 7, 19)
        )
        schueler_in_einrichtung_factory(
            schueler=schueler_factory(),
            einrichtung=einrichtung_factory(),
            eintritt=datetime.date(2016, 7, 14),
            austritt=datetime.date(2016, 7, 19)
        )
        betreuungstage = schueler.angemeldet_in_einrichtung.get_betreuungstage(
            betreuungstage_start,
            betreuungstage_ende
        )
        assert len(betreuungstage) == 2
        assert betreuungstage[schueler_in_einrichtung][0] is betreuungstage_start
        assert len(betreuungstage[schueler_in_einrichtung]) == 2
        assert len(betreuungstage[schueler_in_einrichtung_2]) == 1
        assert betreuungstage[schueler_in_einrichtung_2][0] == betreuungstage_ende - datetime.timedelta(2)
