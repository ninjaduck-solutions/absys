import pytest

from absys.apps.schueler import models


@pytest.mark.django_db
class TestSchuelerQuerySet:

    @pytest.mark.parametrize(('schueler__inaktiv'), [
        (False),
        (True),
    ])
    def test_ist_aktiv_queryset(self, schueler):
        """Stell sicher das ``ist_aktiv`` nur Instanzen mit ``ìnaktiv=False`` liefert."""
        assert (schueler in models.Schueler.objects.ist_aktiv()) is not schueler.inaktiv

    @pytest.mark.parametrize(('schueler__inaktiv'), [
        (False),
        (True),
    ])
    def test_ist_inaktiv_queryset(self, schueler):
        """Stell sicher das ``ist_inaktiv`` nur Instanzen mit ``ìnaktiv=True`` liefert."""
        assert (schueler in models.Schueler.objects.ist_inaktiv()) is schueler.inaktiv
