import factory
from django.utils.timezone import now

from absys.apps.anwesenheitsliste.models import Anwesenheit
from ..einrichtungen.factories import EinrichtungFactory
from ..schueler.factories import SchuelerFactory


class AnwesenheitFactory(factory.DjangoModelFactory):

    schueler = factory.SubFactory(SchuelerFactory)
    einrichtung = factory.SubFactory(EinrichtungFactory)
    datum = factory.LazyAttribute(lambda obj: now().date())
    abwesend = False

    class Meta:
        model = Anwesenheit
