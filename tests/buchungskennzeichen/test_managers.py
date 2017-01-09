import pytest
from django.conf import settings

from absys.apps.buchungskennzeichen import models
from absys.apps.benachrichtigungen.models import BuchungskennzeichenBenachrichtigung


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

    def test_threshhold_unterschritten(self, buchungskennzeichen_factory):
        """Teste das bei Unterschreiten des Schwellwertes eine Benachrichtung erstellt wird."""
        buchungskennzeichen_factory.create_batch(settings.ABSYS_BUCHUNGSKENNZEICHEN_MIN_VERBLEIBEND)
        assert BuchungskennzeichenBenachrichtigung.objects.count() == 0
        models.Buchungskennzeichen.objects.benutzen()
        assert BuchungskennzeichenBenachrichtigung.objects.count() == 1

    def test_threshhold_ueberschritten(self, buchungskennzeichen_factory):
        """Teste das keineBenachrichtung erstellt wird wenn Kennzeichen über Schwellwert."""
        buchungskennzeichen_factory.create_batch(settings.ABSYS_BUCHUNGSKENNZEICHEN_MIN_VERBLEIBEND + 1)
        assert BuchungskennzeichenBenachrichtigung.objects.count() == 0
        models.Buchungskennzeichen.objects.benutzen()
        assert BuchungskennzeichenBenachrichtigung.objects.count() == 0

    def test_keine_buchungskennzeichen(self, buchungskennzeichen_factory):
        """
        Teste das auch dann benachichtigt wird wenn gar keine Kennzeichen vorhanden sind.

        Dies ist insofern ein Sonderfall als das hier sichergestellt wird das die Benachrichtigung
        nicht nur beim 'verbrauchen' eines Kennzeichens erfolgt sondern auch wenn gar keine
        vorhanden sind.
        """
        assert BuchungskennzeichenBenachrichtigung.objects.count() == 0
        models.Buchungskennzeichen.objects.benutzen()
        assert BuchungskennzeichenBenachrichtigung.objects.count() == 1
