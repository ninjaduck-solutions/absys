import datetime

import pytest
from freezegun import freeze_time

from absys.apps.einrichtungen import models


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
    def test_get_betreuungstage(self, schueler, betreuungstage_start, betreuungstage_ende,
            schliesstag, schueler_in_einrichtung, count):
        schliesstag.einrichtungen.set([schueler_in_einrichtung.einrichtung])
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
        schueler_in_einrichtung_2 = schueler_in_einrichtung_factory(
            schueler=schueler,
            einrichtung=einrichtung_factory(),
            eintritt=datetime.date(2016, 7, 14),
            austritt=datetime.date(2016, 7, 19)
        )
        schliesstag_factory(
            datum=datetime.date(2016, 7, 12),
            einrichtungen=[
                schueler_in_einrichtung.einrichtung,
                schueler_in_einrichtung_2.einrichtung,
            ]
        )
        schliesstag_factory(
            datum=datetime.date(2016, 7, 14),
            einrichtungen=[
                schueler_in_einrichtung.einrichtung,
                schueler_in_einrichtung_2.einrichtung,
            ]
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


class TestFerienQuerySet:

    @pytest.mark.django_db
    @freeze_time('2015-06-02 14:00')
    @pytest.mark.parametrize('jahr_gleich', (True, False))
    def test_jahr_start_ende_jahr_identisch(self, ferien, jahr_gleich):
        """Stelle sicher das nur Ferien mit im selben Jahr zurück gegeben werden."""
        if jahr_gleich:
            jahr = ferien.startdatum.year
        else:
            jahr = ferien.startdatum.year - 1
        assert bool(models.Ferien.objects.jahr(jahr)) is jahr_gleich

    @pytest.mark.django_db
    @pytest.mark.parametrize(('jahr', 'erwartung'), ((2015, True), (2016, False)))
    def test_jahr_start_ende_jahr_verschieden(self, ferien_factory, jahr, erwartung):
        """Stelle sicher das nur Ferien mit im selben Jahr zurück agegeben werden."""
        ferien_factory.create(startdatum=datetime.date(2015, 10, 20))
        assert bool(models.Ferien.objects.jahr(jahr)) is erwartung
