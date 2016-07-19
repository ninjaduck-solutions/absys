from django.db import models


class AnwesenheitQuerySet(models.QuerySet):

    def war_abwesend(self, startdatum, enddatum):
        """Abwesenheitstage im gewählten Zeitraum ermitteln."""
        return self.filter(
            datum__range=(startdatum, enddatum),
            abwesend=True
        )
