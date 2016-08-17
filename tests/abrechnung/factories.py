import datetime

import factory

from absys.apps.abrechnung import models
from tests.factories import SchuelerFactory, SozialamtFactory


class RechnungSozialamtFactory(factory.DjangoModelFactory):

    sozialamt = factory.SubFactory(SozialamtFactory)
    startdatum = factory.LazyAttribute(
        lambda obj: obj.enddatum - datetime.timedelta(obj.zeitraum)
    )
    enddatum = datetime.date(2016, 3, 1)

    class Meta:
        model = models.RechnungSozialamt

    class Params:
        zeitraum = 25


class RechnungFactory(factory.DjangoModelFactory):

    rechnung_sozialamt = factory.SubFactory(RechnungSozialamtFactory)
    schueler = factory.SubFactory(SchuelerFactory)
    fehltage_gesamt = 10

    class Meta:
        model = models.Rechnung
