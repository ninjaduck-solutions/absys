import datetime

import factory
from django.utils.timezone import now

from absys.apps.abrechnung import models
from tests.factories import SchuelerFactory, SozialamtFactory


class RechnungSozialamtFactory(factory.DjangoModelFactory):

    sozialamt = factory.SubFactory(SozialamtFactory)
    startdatum = factory.LazyAttribute(lambda obj: now().date())
    enddatum = factory.LazyAttribute(
        lambda obj: obj.startdatum + datetime.timedelta(obj.zeitraum)
    )

    class Meta:
        model = models.RechnungSozialamt

    class Params:
        zeitraum = 25


class RechnungFactory(factory.DjangoModelFactory):

    rechnung_sozialamt = factory.SubFactory(RechnungSozialamtFactory)
    schueler = factory.SubFactory(SchuelerFactory)

    class Meta:
        model = models.Rechnung
