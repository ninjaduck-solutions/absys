import datetime

import factory
from django.utils.timezone import now

from absys.apps.einrichtungen import models
from ..schueler.factories import SchuelerFactory


class SchliesstagFactory(factory.DjangoModelFactory):

    name = factory.Faker('word')
    datum = factory.LazyAttribute(lambda obj: now().date())
    art = "Test"

    @factory.post_generation
    def einrichtungen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for einrichtung in extracted:
                self.einrichtungen.add(einrichtung)

    class Meta:
        model = models.Schliesstag


class StandortFactory(factory.DjangoModelFactory):

    anschrift = factory.Faker('address')
    konto_iban = factory.Faker('pyint')
    konto_bic = factory.Faker('pyint')
    konto_institut = factory.Faker('pyint')

    class Meta:
        model = models.Standort


class EinrichtungFactory(factory.DjangoModelFactory):

    name = factory.Faker('word')
    kuerzel = factory.Sequence(lambda n: '{0}{1}'.format('E', n))
    standort = factory.SubFactory(StandortFactory)
    titel = factory.Sequence(lambda n: n)

    @factory.post_generation
    def schueler(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            raise NotImplementedError()

    class Meta:
        model = models.Einrichtung


class EinrichtungHatPflegesatzFactory(factory.DjangoModelFactory):

    einrichtung = factory.SubFactory(EinrichtungFactory)
    pflegesatz = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    pflegesatz_ferien = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    pflegesatz_startdatum = factory.LazyAttribute(lambda obj: now().date())
    pflegesatz_enddatum = factory.LazyAttribute(
        lambda obj: obj.pflegesatz_startdatum + datetime.timedelta(obj.pflegesatz_dauer)
    )

    class Meta:
        model = models.EinrichtungHatPflegesatz

    class Params:
        pflegesatz_dauer = 25


class SchuelerInEinrichtungFactory(factory.DjangoModelFactory):

    schueler = factory.SubFactory(SchuelerFactory)
    einrichtung = factory.SubFactory(EinrichtungFactory)
    eintritt = factory.LazyAttribute(lambda obj: now().date())
    austritt = factory.LazyAttribute(lambda obj: obj.eintritt + datetime.timedelta(obj.tage_angemeldet))
    pers_pflegesatz = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    pers_pflegesatz_ferien = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    pers_pflegesatz_startdatum = factory.LazyAttribute(lambda obj: now().date())
    pers_pflegesatz_enddatum = factory.LazyAttribute(
        lambda obj: obj.pers_pflegesatz_startdatum + datetime.timedelta(obj.tage_pers_pflegesatz)
    )
    fehltage_erlaubt = 5

    class Meta:
        model = models.SchuelerInEinrichtung

    class Params:
        tage_angemeldet = 25
        tage_pers_pflegesatz = 10


class SchuelerAngemeldetInEinrichtungFactory(SchuelerFactory):

    angemeldet = factory.RelatedFactory(SchuelerInEinrichtungFactory, 'schueler')


class FerienFactory(factory.DjangoModelFactory):

    name = factory.Faker('word')
    startdatum = factory.LazyAttribute(lambda obj: now().date())
    enddatum = factory.LazyAttribute(lambda obj: obj.startdatum + datetime.timedelta(obj.dauer))

    @factory.post_generation
    def einrichtungen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for einrichtung in extracted:
                self.einrichtungen.add(einrichtung)

    class Meta:
        model = models.Ferien

    class Params:
        dauer = 15
