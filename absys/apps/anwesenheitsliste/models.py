from django.db import models

from absys.apps.schueler.models import Schueler

from . import managers


class Anwesenheit(models.Model):

    schueler = models.ForeignKey(Schueler, verbose_name="Schüler", related_name='anwesenheit',
        on_delete=models.CASCADE)
    datum = models.DateField("Datum", db_index=True)
    abwesend = models.BooleanField("Abwesend", default=False)

    objects = managers.AnwesenheitQuerySet.as_manager()

    class Meta:
        verbose_name = "Anwesenheit"
        verbose_name_plural = "Anwesenheiten"
        ordering = ['datum', 'schueler']
        unique_together = ('schueler', 'datum')

    def __str__(self):
        if self.pk:
            return "{s.schueler} am {s.datum}".format(s=self)
        else:
            return str(self.datum)
