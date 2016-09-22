import datetime
import random

import factory
from django.utils.timezone import now

from absys.apps.abrechnung import models
from ..einrichtungen.factories import EinrichtungFactory
from ..schueler.factories import SchuelerFactory, SozialamtFactory


class RechnungSozialamtFactory(factory.DjangoModelFactory):

    sozialamt = factory.SubFactory(SozialamtFactory)
    startdatum = factory.LazyAttribute(
        lambda obj: obj.enddatum - datetime.timedelta(obj.zeitraum)
    )
    enddatum = datetime.date(2016, 3, 31)

    class Meta:
        model = models.RechnungSozialamt

    class Params:
        zeitraum = 30


class RechnungsPositionSchuelerFactory(factory.DjangoModelFactory):

    rechnung_sozialamt = factory.SubFactory(RechnungSozialamtFactory)
    schueler = factory.SubFactory(SchuelerFactory)
    einrichtung = factory.SubFactory(EinrichtungFactory)
    pflegesatz = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    datum = factory.LazyAttribute(lambda obj: now().date() - datetime.timedelta(random.randint(10, 30)))

    class Meta:
        model = models.RechnungsPositionSchueler
