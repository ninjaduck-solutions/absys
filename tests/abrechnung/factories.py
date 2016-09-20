import datetime

import factory

from absys.apps.abrechnung import models
from tests.factories import EinrichtungFactory, SchuelerFactory, SozialamtFactory


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

    class Meta:
        model = models.RechnungsPositionSchueler
