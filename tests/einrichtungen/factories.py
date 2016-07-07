import factory

from absys.apps.einrichtungen import models


class SchliesstagFactory(factory.DjangoModelFactory):

    name = factory.Faker('word')
    datum = factory.Faker('date')
    art = "Test"

    class Meta:
        model = models.Schliesstag
