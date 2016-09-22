import pytest

from absys.apps.buchungskennzeichen import models


@pytest.mark.django_db
class TestBuchungskennzeichenManager:

    def test_benutzen(self, buchungskennzeichen_factory):
        buchungskennzeichen_1 = '0554.0019.0096'
        buchungskennzeichen_factory.create(buchungskennzeichen=buchungskennzeichen_1)
        buchungskennzeichen_2 = '0554.0019.0097'
        buchungskennzeichen_factory.create(buchungskennzeichen=buchungskennzeichen_2)
        models.Buchungskennzeichen.objects.filter(verfuegbar=True).count() == 2
        assert models.Buchungskennzeichen.objects.benutzen() == buchungskennzeichen_1
        models.Buchungskennzeichen.objects.filter(verfuegbar=True).count() == 1
        assert models.Buchungskennzeichen.objects.benutzen() == buchungskennzeichen_2
        models.Buchungskennzeichen.objects.filter(verfuegbar=False).count() == 2
        assert models.Buchungskennzeichen.objects.benutzen() == ''
