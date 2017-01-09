import pytest

from absys.apps.benachrichtigungen import models


@pytest.mark.django_db
class TestBuchungsKennzeichenBenachrichtigungManager():

    def test_benachrichtigen_neu(self):
        """Teste das eine Benachrichtigung erstellt."""
        assert models.BuchungskennzeichenBenachrichtigung.objects.count() == 0
        models.BuchungskennzeichenBenachrichtigung.objects.benachrichtige()
        assert models.BuchungskennzeichenBenachrichtigung.objects.count() == 1

    @pytest.mark.parametrize(('buchungskennzeichen_benachrichtigung__erledigt', 'erwartung'),
        ((True, False), (False, True)))
    def test__vorhanden(self, buchungskennzeichen_benachrichtigung, erwartung):
        result = models.BuchungskennzeichenBenachrichtigung.objects._vorhanden()
        assert bool(result) is erwartung


@pytest.mark.django_db
class TestSchuelerInEinrichtungLaeuftAusBenachrichtigungManager():

    def test_benachrichtigen_neu(self, schueler_in_einrichtung):
        """Teste das eine Benachrichtigung erstellt."""
        assert models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects.count() == 0
        result = models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects.benachrichtige(schueler_in_einrichtung)
        assert models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects.count() == 1
        assert result.schueler_in_einrichtung == schueler_in_einrichtung

    @pytest.mark.parametrize(('schueler_in_einrichtung_laeuft_aus_benachrichtigung__erledigt', 'erwartung'),
        ((True, False), (False, True)))
    def test__vorhanden_erledigt(self, schueler_in_einrichtung_laeuft_aus_benachrichtigung, erwartung):
        schueler_in_einrichtung = schueler_in_einrichtung_laeuft_aus_benachrichtigung.schueler_in_einrichtung
        result = models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects._vorhanden(schueler_in_einrichtung)
        assert bool(result) is erwartung

    @pytest.mark.parametrize('selber_schueler', (True, False))
    def test__vorhanden_selbers_inhalt(self, schueler_in_einrichtung_laeuft_aus_benachrichtigung, schueler_in_einrichtung_factory, selber_schueler):
        if selber_schueler:
            schueler_in_einrichtung = schueler_in_einrichtung_laeuft_aus_benachrichtigung.schueler_in_einrichtung
        else:
            schueler_in_einrichtung = schueler_in_einrichtung_factory.create()
        result = models.SchuelerInEinrichtungLaeuftAusBenachrichtigung.objects._vorhanden(schueler_in_einrichtung)
        assert bool(result) is selber_schueler


@pytest.mark.django_db
class TestEinrichtunghatPflegesatzLaeuftAusBenachrichtigungManager():

    def test_benachrichtigen_neu(self, einrichtung_hat_pflegesatz):
        """Teste das eine Benachrichtigung erstellt."""
        assert models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects.count() == 0
        result = models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects.benachrichtige(einrichtung_hat_pflegesatz)
        assert models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects.count() == 1
        assert result.einrichtung_hat_pflegesatz == einrichtung_hat_pflegesatz

    @pytest.mark.parametrize(
        ('einrichtung_hat_pflegesatz_laeuft_aus_benachrichtigung__erledigt', 'erwartung'),
        ((True, False), (False, True)))
    def test__vorhanden_erledigt(self, einrichtung_hat_pflegesatz_laeuft_aus_benachrichtigung, erwartung):
        einrichtung_hat_pflegesatz = einrichtung_hat_pflegesatz_laeuft_aus_benachrichtigung.einrichtung_hat_pflegesatz
        result = models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects._vorhanden(einrichtung_hat_pflegesatz)
        assert bool(result) is erwartung

    @pytest.mark.parametrize('selbe_einrichtung_hat_pflegesatz', (True, False))
    def test__vorhanden_selber_inhalt(self, einrichtung_hat_pflegesatz_laeuft_aus_benachrichtigung, einrichtung_hat_pflegesatz_factory, selbe_einrichtung_hat_pflegesatz):
        if selbe_einrichtung_hat_pflegesatz:
            einrichtung_hat_pflegesatz = einrichtung_hat_pflegesatz_laeuft_aus_benachrichtigung.einrichtung_hat_pflegesatz
        else:
            einrichtung_hat_pflegesatz = einrichtung_hat_pflegesatz_factory.create()
        result = models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung.objects._vorhanden(einrichtung_hat_pflegesatz)
        assert bool(result) is selbe_einrichtung_hat_pflegesatz


@pytest.mark.django_db
class TestBettensatzLaeuftAusBenachrichtigungManager():

    def test_benachrichtigen_neu(self, bettengeldsatz):
        """Teste das eine Benachrichtigung erstellt."""
        assert models.BettengeldsatzLaeuftAusBenachrichtigung.objects.count() == 0
        result = models.BettengeldsatzLaeuftAusBenachrichtigung.objects.benachrichtige(bettengeldsatz)
        assert models.BettengeldsatzLaeuftAusBenachrichtigung.objects.count() == 1
        assert result.bettengeldsatz == bettengeldsatz

    @pytest.mark.parametrize(
        ('bettengeldsatz_laeuft_aus_benachrichtigung__erledigt', 'erwartung'),
        ((True, False), (False, True)))
    def test__vorhanden_erledigt(self, bettengeldsatz_laeuft_aus_benachrichtigung, erwartung):
        bettengeldsatz = bettengeldsatz_laeuft_aus_benachrichtigung.bettengeldsatz
        result = models.BettengeldsatzLaeuftAusBenachrichtigung.objects._vorhanden(bettengeldsatz)
        assert bool(result) is erwartung

    @pytest.mark.parametrize('selber_bettengeldsatz', (True, False))
    def test__vorhanden_selber_inhalt(self, bettengeldsatz_laeuft_aus_benachrichtigung, bettengeldsatz_factory, selber_bettengeldsatz):
        if selber_bettengeldsatz:
            bettengeldsatz = bettengeldsatz_laeuft_aus_benachrichtigung.bettengeldsatz
        else:
            bettengeldsatz = bettengeldsatz_factory.create()
        result = models.BettengeldsatzLaeuftAusBenachrichtigung.objects._vorhanden(bettengeldsatz)
        assert bool(result) is selber_bettengeldsatz


@pytest.mark.django_db
class TestFerienBenachrichtigungManager():

    def test_benachrichtigen_neu(self, einrichtung):
        """Teste das eine Benachrichtigung erstellt."""
        assert models.FerienBenachrichtigung.objects.count() == 0
        result = models.FerienBenachrichtigung.objects.benachrichtige(einrichtung, 2015)
        assert models.FerienBenachrichtigung.objects.count() == 1
        assert result.einrichtung == einrichtung

    @pytest.mark.parametrize(
        ('ferien_benachrichtigung__erledigt', 'erwartung'),
        ((True, False), (False, True)))
    def test__vorhanden_erledigt(self, ferien_benachrichtigung, erwartung):
        einrichtung = ferien_benachrichtigung.einrichtung
        jahr = ferien_benachrichtigung.jahr
        result = models.FerienBenachrichtigung.objects._vorhanden(einrichtung, jahr)
        assert bool(result) is erwartung

    @pytest.mark.parametrize(('selbe_einrichtung', 'selbes_jahr'), (
        (True, True), (True, False), (False, True), (False, False),
    ))
    def test__vorhanden_selber_inhalt(self, ferien_benachrichtigung, einrichtung_factory,
                                      selbe_einrichtung, selbes_jahr):
        if selbe_einrichtung:
            einrichtung = ferien_benachrichtigung.einrichtung
        else:
            einrichtung = einrichtung_factory.create()

        if selbes_jahr:
            jahr = ferien_benachrichtigung.jahr
        else:
            jahr = int(ferien_benachrichtigung.jahr) - 1

        result = models.FerienBenachrichtigung.objects._vorhanden(einrichtung, jahr)
        assert bool(result) is (selbe_einrichtung and selbes_jahr)


@pytest.mark.django_db
class TestSchliesstageBenachrichtigungManager():

    def test_benachrichtigen_neu(self, einrichtung):
        """Teste das eine Benachrichtigung erstellt."""
        assert models.SchliesstageBenachrichtigung.objects.count() == 0
        result = models.SchliesstageBenachrichtigung.objects.benachrichtige(einrichtung, 2015)
        assert models.SchliesstageBenachrichtigung.objects.count() == 1
        assert result.einrichtung == einrichtung

    @pytest.mark.parametrize(
        ('schliesstage_benachrichtigung__erledigt', 'erwartung'),
        ((True, False), (False, True)))
    def test__vorhanden_erledigt(self, schliesstage_benachrichtigung, erwartung):
        einrichtung = schliesstage_benachrichtigung.einrichtung
        jahr = schliesstage_benachrichtigung.jahr
        result = models.SchliesstageBenachrichtigung.objects._vorhanden(einrichtung, jahr)
        assert bool(result) is erwartung

    @pytest.mark.parametrize(('selbe_einrichtung', 'selbes_jahr'), (
        (True, True), (True, False), (False, True), (False, False),
    ))
    def test__vorhanden_selber_inhalt(self, schliesstage_benachrichtigung, einrichtung_factory,
                                      selbe_einrichtung, selbes_jahr):
        if selbe_einrichtung:
            einrichtung = schliesstage_benachrichtigung.einrichtung
        else:
            einrichtung = einrichtung_factory.create()

        if selbes_jahr:
            jahr = schliesstage_benachrichtigung.jahr
        else:
            jahr = int(schliesstage_benachrichtigung.jahr) - 1

        result = models.SchliesstageBenachrichtigung.objects._vorhanden(einrichtung, jahr)
        assert bool(result) is (selbe_einrichtung and selbes_jahr)
