import datetime

import pytest
from django.utils.timezone import now

from absys.apps.benachrichtigungen import services, models


@pytest.mark.django_db
class TestPruefeSchuelerInEinrichtung():

    def test_pruefe_schueler_in_einrichtung_keine(self):
        """
        Teste das bei fehlenden ``SchuelerInEinrichtung``en keine Benachichtigung erstellt wird.
        """
        services.pruefe_schueler_in_einrichtung()
        assert models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects.count() == 0

    @pytest.mark.parametrize(('austritt_laeuft_aus', 'pers_pflegesatz_laeuft_aus', 'erwartung'), (
        (True, True, True), (False, True, True), (True, False, True), (False, False, False)
    ))
    def test_pruefe_schueler_in_einrichtung_keine_aktuellen(self,
            schueler_in_einrichtung_factory, austritt_laeuft_aus,
            pers_pflegesatz_laeuft_aus, erwartung):
        """Teste verschiedene``austritt`` und ``pers_pflegesatz_enddatum`` Kombinationen."""

        schueler_in_einrichtung_factory(austritt_laeuft_aus=austritt_laeuft_aus,
            pers_pflegesatz_laeuft_aus=pers_pflegesatz_laeuft_aus)
        services.pruefe_schueler_in_einrichtung()
        assert bool(models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects.count()) == (
            erwartung
        )


@pytest.mark.django_db
class TestPruefeEinrichtungHatPflegesatz():

    def test_pruefe_einrichtung_hat_pflegesatz(self):
        """
        Teste das bei fehlenden ``EinrichtungHatPflegesatz``en keine Benachichtigung erstellt wird.
        """
        services.pruefe_einrichtung_hat_pflegesatz()
        assert models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects.count() == 0

    @pytest.mark.parametrize('laeuft_aus', (True, False))
    def test_pruefe_einrichtung_hat_pflegesatz_benachrichtigen(self,
            einrichtung_hat_pflegesatz_factory, laeuft_aus):
        """
        Teste das je nach 'Ablaufzustand' einer ``EinrichtungHatPflegesatz`` benachrichtigt wird.
        """
        einrichtung_hat_pflegesatz_factory(laeuft_aus=laeuft_aus)
        services.pruefe_einrichtung_hat_pflegesatz()
        assert bool(models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects.count()) == (
            laeuft_aus
        )


@pytest.mark.django_db
class TestPruefeBettengeldsatz():

    def test_pruefe_bettengeldsatz(self):
        """
        Teste das bei fehlenden ``Bettengeldsatz``en keine Benachichtigung erstellt wird.
        """
        services.pruefe_bettengeldsatz()
        assert models.BettengeldsatzLaeuftAusBenachrichtigung.objects.count() == 0

    @pytest.mark.parametrize('laeuft_aus', (True, False))
    def test_pruefe_bettengeldsatz_benachrichtigen(self, bettengeldsatz_factory, laeuft_aus):
        """
        Teste das je nach 'Ablaufzustand' eines ``Bettensatz``es benachrichtigt wird.
        """
        bettengeldsatz_factory(laeuft_aus=laeuft_aus)
        services.pruefe_bettengeldsatz()
        assert bool(models.BettengeldsatzLaeuftAusBenachrichtigung.objects.count()) == laeuft_aus


@pytest.mark.django_db
class TestPruefeFerien():

    @pytest.mark.django_db
    def test_pruefe_ferien(self):
        """
        Teste das bei fehlenden ``Ferien`` keine Benachichtigung erstellt wird.
        """
        services.pruefe_ferien()
        assert models.FerienBenachrichtigung.objects.count() == 0

    @pytest.mark.parametrize(('start_vorjahr', 'ende_folgejahr', 'erwartung'), (
        (True, True, 1), (True, False, 1), (False, True, 1), (False, False, 0)
    ))
    def test_pruefe_ferien_benachrichtigen(self, ferien_factory, einrichtung,
            start_vorjahr, ende_folgejahr, erwartung):
        """
        Teste das Benachrichtigungen nur erstelt werden wenn Ferien nicht im selben Jahr.

        Ferien sind nur dann 'im selben Jahr' wenn Anfang *und* ende im selben Jahr sind.
        Daher parametrisieren wir über verschiedene Versionen.
        """
        ferien_factory(start_vorjahr=start_vorjahr, ende_folgejahr=ende_folgejahr,
            einrichtungen=[einrichtung])
        services.pruefe_ferien()
        assert models.FerienBenachrichtigung.objects.count() == erwartung


@pytest.mark.django_db
class TestPruefeSchliesstage():

    @pytest.mark.django_db
    def test_pruefe_schliesstage(self):
        """
        Teste das bei fehlenden ``Schliesstage``en keine Benachichtigung erstellt wird.
        """
        services.pruefe_schliesstage()
        assert models.SchliesstageBenachrichtigung.objects.count() == 0

    @pytest.mark.parametrize('vorjahr', (True, False))
    def test_pruefe_schliesstage_benachrichtigen(self, schliesstag_factory, einrichtung, vorjahr):
        """
        Teste das Benachrichtigungen nur erstelt werden wenn Schliesstage nicht im selben Jahr.
        """
        schliesstag_factory(vorjahr=vorjahr, einrichtungen=[einrichtung])
        services.pruefe_schliesstage()
        assert bool(models.SchliesstageBenachrichtigung.objects.count()) is vorjahr
