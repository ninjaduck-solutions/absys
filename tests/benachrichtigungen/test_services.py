import datetime

import pytest
from django.utils.timezone import now

from absys.apps.benachrichtigungen import services, models


class TestPruefeSchuelerInEinrichtung():

    @pytest.mark.django_db
    def test_pruefe_schueler_in_einrichtung_keine(self):
        services.pruefe_schueler_in_einrichtung()
        assert models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects.count() == 0

    @pytest.mark.django_db
    @pytest.mark.parametrize(('austritt_offset', 'pflegesatz_offset', 'erwartung'), (
        # Nur ``.austritt``
        (0, None, True), (29, None, True), (30, None, False), (40, None, False),
        # Nur ``per_pflegesatz_enddatum``
        (40, 0, True), (40, 29, True), (40, 30, False), (40, 40, False),
    ))
    def test_pruefe_schueler_in_einrichtung_keine_aktuellen(self, schueler_in_einrichtung_factory,
            austritt_offset, pflegesatz_offset, erwartung):
        """Es gibt keine ``SchuelerInEinrichtung`` mit ``autritt > heute``."""
        austritt = datetime.date.today() + datetime.timedelta(austritt_offset)

        if pflegesatz_offset is None:
            pflegesatz_enddatum = None
        else:
            pflegesatz_enddatum = datetime.date.today() + datetime.timedelta(pflegesatz_offset)

        schueler_in_einrichtung_factory(austritt=austritt,
            pers_pflegesatz_enddatum=pflegesatz_enddatum)
        services.pruefe_schueler_in_einrichtung()
        assert bool(models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects.count()) == erwartung


class TestPruefeEinrichtungHatPflegesatz():

    @pytest.mark.django_db
    def test_pruefe_einrichtung_hat_pflegesatz(self):
        services.pruefe_einrichtung_hat_pflegesatz()
        assert models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects.count() == 0

    @pytest.mark.django_db
    @pytest.mark.parametrize(('offset', 'erwartung'), (
        (0, True), (29, True), (30, False), (40, False),
    ))
    def test_pruefe_einrichtung_hat_pflegesatz_benachrichtigen(self,
            einrichtung_hat_pflegesatz_factory, offset, erwartung):
        if offset is None:
            enddatum = None
        else:
            enddatum = datetime.date.today() + datetime.timedelta(offset)
        einrichtung_hat_pflegesatz_factory(pflegesatz_enddatum=enddatum)
        services.pruefe_einrichtung_hat_pflegesatz()
        assert bool(models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects.count()) == erwartung


class TestPruefeBettengeldsatz():

    @pytest.mark.django_db
    def test_pruefe_bettengeldsatz(self):
        services.pruefe_bettengeldsatz()
        assert models.BettengeldsatzLaeuftAusBenachrichtigung.objects.count() == 0

    @pytest.mark.django_db
    @pytest.mark.parametrize(('offset', 'erwartung'), (
        (0, True), (29, True), (30, False), (40, False),
    ))
    def test_pruefe_bettengeldsatz_benachrichtigen(self, bettengeldsatz_factory, offset,
            erwartung):
        if offset is None:
            enddatum = None
        else:
            enddatum = datetime.date.today() + datetime.timedelta(offset)
        bettengeldsatz_factory(enddatum=enddatum)
        services.pruefe_bettengeldsatz()
        assert bool(models.BettengeldsatzLaeuftAusBenachrichtigung.objects.count()) == erwartung


class TestPruefeFerien():

    @pytest.mark.django_db
    def test_pruefe_ferien(self):
        services.pruefe_ferien()
        assert models.FerienBenachrichtigung.objects.count() == 0

    @pytest.mark.django_db
    @pytest.mark.parametrize('selbes_jahr', (True, False))
    def test_pruefe_ferien_benachrichtigen(self, ferien_factory, einrichtung, selbes_jahr):
        jahr = now().year
        if selbes_jahr:
            ferien_factory(startdatum=datetime.date(jahr, 2, 1), einrichtungen=[einrichtung])
        else:
            ferien_factory(startdatum=datetime.date(2012, 2, 1), einrichtungen=[einrichtung])

        services.pruefe_ferien()
        assert bool(models.FerienBenachrichtigung.objects.count()) is not selbes_jahr


class TestPruefeSchliesstage():

    @pytest.mark.django_db
    def test_pruefe_schliesstage(self):
        services.pruefe_schliesstage()
        assert models.SchliesstageBenachrichtigung.objects.count() == 0

    @pytest.mark.django_db
    @pytest.mark.parametrize('selbes_jahr', (True, False))
    def test_pruefe_schliesstage_benachrichtigen(self, schliesstag_factory, einrichtung, selbes_jahr):
        jahr = now().year
        if selbes_jahr:
            schliesstag_factory(datum=datetime.date(jahr, 2, 1), einrichtungen=[einrichtung])
        else:
            schliesstag_factory(datum=datetime.date(2012, 2, 1), einrichtungen=[einrichtung])

        services.pruefe_schliesstage()
        assert bool(models.SchliesstageBenachrichtigung.objects.count()) is not selbes_jahr
