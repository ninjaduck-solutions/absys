from django.db import models
from model_utils.models import TimeStampedModel

from . import managers


class Buchungskennzeichen(TimeStampedModel):
    """
    Sammlung von Buchungskennzeichen.

    Buchungskennzeichen werden manuell eingepflegt und bei der Erstellung von
    :model:`abrechnung.RechnungEinrichtung`-Instanzen genutzt. Benutzte
    Buchungskennzeichen werden als nicht mehr verfügbar markiert, damit sie
    nicht noch einmal verwendet werden können.
    """

    buchungskennzeichen = models.CharField("Buchungskennzeichen", max_length=20, unique=True,
        help_text="Bitte das Buchungskennzeichen ohne Trennpunkte eingeben.")
    verfuegbar = models.BooleanField("ist verfügbar", default=True, editable=False)

    objects = managers.BuchungskennzeichenManager()

    class Meta:
        ordering = ['-created']
        verbose_name = "Buchungskennzeichen"
        verbose_name_plural = "Buchungskennzeichen"

    def __str__(self):
        return self.buchungskennzeichen
