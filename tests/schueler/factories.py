import factory
from django.utils.timezone import now

from absys.apps.schueler.models import Gruppe, Sozialamt, Schueler


class GruppeFactory(factory.DjangoModelFactory):

    name = factory.Faker('word')

    class Meta:
        model = Gruppe


class SozialamtFactory(factory.DjangoModelFactory):

    name = factory.Faker('word')
    anschrift = factory.Faker('address')
    konto_iban = factory.Faker('pyint')
    konto_bic = factory.Faker('pyint')
    konto_institut = factory.Faker('pyint')

    class Meta:
        model = Sozialamt


class SchuelerFactory(factory.DjangoModelFactory):

    vorname = factory.Faker('first_name')
    nachname = factory.Faker('last_name')
    geburtsdatum = factory.LazyAttribute(lambda obj: now().date())
    gruppe = factory.SubFactory(GruppeFactory)
    sozialamt = factory.SubFactory(SozialamtFactory)

    class Meta:
        model = Schueler
