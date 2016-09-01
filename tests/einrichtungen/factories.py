import factory
from django.utils.timezone import now

from absys.apps.einrichtungen import models


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
