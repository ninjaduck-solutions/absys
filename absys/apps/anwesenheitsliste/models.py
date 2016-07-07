from django.db import models

from absys.apps.einrichtungen.models import Einrichtung
from absys.apps.schueler.models import Schueler


class Anwesenheit(models.Model):

    schueler = models.ForeignKey(Schueler, verbose_name="Schüler", related_name='anwesenheit')
    einrichtung = models.ForeignKey(Einrichtung, verbose_name="Einrichtung")
    datum = models.DateField("Datum", db_index=True)
    abwesend = models.BooleanField("Abwesend", default=False)

    class Meta:
        verbose_name = "Anwesenheit"
        verbose_name_plural = "Anwesenheiten"
        ordering = ['datum', 'schueler']
        unique_together = ('schueler', 'einrichtung', 'datum')

    def __str__(self):
        return "{s.schueler} in {s.einrichtung} am {s.datum}".format(s=self)
