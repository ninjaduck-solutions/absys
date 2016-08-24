import datetime

import pytest


@pytest.mark.django_db
class TestSchuelerInEinrichtungQuerySet:

    @pytest.mark.parametrize((
        'schliesstag__datum',
        'schueler_in_einrichtung__eintritt',
        'schueler_in_einrichtung__austritt',
        'count'
    ), [
        (  # Eintritt vor Start, Austritt nach Ende, ein Schließ­tag
            datetime.date(2016, 7, 12),
            datetime.date(2016, 7, 1),
            datetime.date(2016, 7, 31),
            4
        ),
        (  # Eintritt vor Start, Austritt nach Ende, kein Schließ­tag
            datetime.date(2016, 6, 2),
            datetime.date(2016, 7, 1),
            datetime.date(2016, 7, 31),
            5
        ),
        (  # Eintritt am Start, Austritt am Ende, kein Schließ­tag
            datetime.date(2016, 6, 2),
            datetime.date(2016, 7, 11),
            datetime.date(2016, 7, 17),
            5
        ),
        (  # Eintritt vor Start, Austritt am Ende, kein Schließ­tag
            datetime.date(2016, 6, 2),
            datetime.date(2016, 7, 1),
            datetime.date(2016, 7, 17),
            5
        ),
        (  # Eintritt nach Start, Austritt vor Ende, kein Schließ­tag
            datetime.date(2016, 6, 2),
            datetime.date(2016, 7, 12),
            datetime.date(2016, 7, 14),
            3
        ),
        (  # Eintritt am Start, Austritt nach Ende, kein Schließ­tag
            datetime.date(2016, 6, 2),
            datetime.date(2016, 7, 11),
            datetime.date(2016, 7, 31),
            5
        ),
        (  # Eintritt vor Start, Austritt vor Ende, kein Schließ­tag
            datetime.date(2016, 6, 2),
            datetime.date(2016, 6, 15),
            datetime.date(2016, 7, 14),
            4
        ),
        (  # Eintritt nach Start, Austritt nach Ende, kein Schließ­tag
            datetime.date(2016, 6, 2),
            datetime.date(2016, 7, 12),
            datetime.date(2016, 7, 31),
            4
        ),
        (  # Schueler im Zeitraum nicht in Einrichtung
            datetime.date(2015, 7, 12),
            datetime.date(2015, 7, 1),
            datetime.date(2015, 7, 31),
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
        if count:
            assert len(betreuungstage) == 1
        else:
            assert len(betreuungstage) == 0
        for schueler_in_einrichtung, tage in betreuungstage.items():
            assert schueler_in_einrichtung.schueler == schueler
            assert len(tage) == count
            assert (
                (tage[0] == betreuungstage_start) |
                (tage[0] == schueler_in_einrichtung.eintritt) |
                (tage[-1] == betreuungstage_ende) |
                (tage[-1] == schueler_in_einrichtung.austritt)
            )

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
