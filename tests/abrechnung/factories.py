import datetime

import factory
from django.utils.timezone import now

from absys.apps.abrechnung.models import Rechnung
from tests.factories import SchuelerFactory, SozialamtFactory


class RechnungFactory(factory.DjangoModelFactory):

    sozialamt = factory.SubFactory(SozialamtFactory)
    schueler = factory.SubFactory(SchuelerFactory)
    startdatum = factory.LazyAttribute(lambda obj: now().date())
    enddatum = factory.LazyAttribute(
        lambda obj: obj.startdatum + datetime.timedelta(obj.zeitraum)
    )

    class Meta:
        model = Rechnung

    class Params:
        zeitraum = 25
