import factory

from absys.apps.benachrichtigungen import models
from ..einrichtungen.factories import (SchuelerInEinrichtungFactory,
                                       EinrichtungHatPflegesatzFactory,
                                       BettengeldsatzFactory, EinrichtungFactory)


class BuchungskennzeichenBenachrichtigungFactory(factory.DjangoModelFactory):

    erledigt = False

    class Meta:
        model = models.BuchungskennzeichenBenachrichtigung


class SchuelerInEinrichtungLaeuftAusBenachrichtigungFactory(factory.DjangoModelFactory):

    schueler_in_einrichtung = factory.SubFactory(SchuelerInEinrichtungFactory)
    erledigt = False

    class Meta:
        model = models.SchuelerInEinrichtungLaeuftAusBenachrichtigung


class EinrichtungHatPflegesatzLaeuftAusBenachrichtigungFactory(factory.DjangoModelFactory):

    einrichtung_hat_pflegesatz = factory.SubFactory(EinrichtungHatPflegesatzFactory)
    erledigt = False

    class Meta:
        model = models.EinrichtungHatPflegesatzLaeuftAusBenachrichtigung


class BettengeldsatzLaeuftAusBenachrichtigungFactory(factory.DjangoModelFactory):

    bettengeldsatz = factory.SubFactory(BettengeldsatzFactory)
    erledigt = False

    class Meta:
        model = models.BettengeldsatzLaeuftAusBenachrichtigung


class FerienBenachrichtigungFactory(factory.DjangoModelFactory):

    einrichtung = factory.SubFactory(EinrichtungFactory)
    jahr = factory.Faker('year')
    erledigt = False

    class Meta:
        model = models.FerienBenachrichtigung


class SchliesstageBenachrichtigungFactory(factory.DjangoModelFactory):

    einrichtung = factory.SubFactory(EinrichtungFactory)
    jahr = factory.Faker('year')
    erledigt = False

    class Meta:
        model = models.SchliesstageBenachrichtigung
