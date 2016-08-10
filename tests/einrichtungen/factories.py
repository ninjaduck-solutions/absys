import factory
from django.utils.timezone import now

from absys.apps.einrichtungen import models


class SchliesstagFactory(factory.DjangoModelFactory):

    name = factory.Faker('word')
    datum = factory.LazyAttribute(lambda obj: now().date())
    art = "Test"

    class Meta:
        model = models.Schliesstag
