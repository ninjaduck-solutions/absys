from django.db import models
from model_utils.models import TimeStampedModel

from absys.apps.schueler.models import Schueler

# TODO: CONSTRAINTS mit clean() (siehe ModelValidation in DjangoDocs)


class Einrichtung(TimeStampedModel):

    name = models.CharField("Name", max_length=30, unique=True)
    kuerzel = models.CharField("Kürzel", max_length=1, unique=True)
    schueler = models.ManyToManyField(
        Schueler,
        verbose_name='Schüler',
        through='SchuelerInEinrichtung',
        related_name='einrichtungen'
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Einrichtung"
        verbose_name_plural = "Einrichtungen"

    def __str__(self):
        return self.name


class SchuelerInEinrichtung(TimeStampedModel):

    schueler = models.ForeignKey(Schueler)
    einrichtung = models.ForeignKey(Einrichtung)
    eintritt = models.DateField()
    austritt = models.DateField()
    sozialamtbescheid_von = models.DateField()
    sozialamtbescheid_bis = models.DateField()
    pers_pflegesatz = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    pers_pflegesatz_startdatum = models.DateField(blank=True)
    pers_pflegesatz_enddatum = models.DateField(blank=True)
    pers_pflegesatz_ferien = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    pers_pflegesatz_ferien_startdatum = models.DateField(blank=True)
    pers_pflegesatz_ferien_enddatum = models.DateField(blank=True)

    class Meta:
        ordering = ("schueler__nachname", "schueler__vorname", "-austritt")
        unique_together = ('schueler', 'einrichtung', 'eintritt', 'austritt')
        verbose_name = "Schueler in der Einrichtung"
        verbose_name_plural = "Schueler in den Einrichtungen"

    def __str__(self):
        return '{s.schueler} in {s.einrichtung} ({s.eintritt} - {s.austritt}) '.format(s=self)


class EinrichtungHatPflegesatz(TimeStampedModel):

    name = models.ForeignKey(Einrichtung, related_name='pflegesaetze')
    pflegesatz = models.DecimalField(max_digits=4, decimal_places=2)
    pflegesatz_startdatum = models.DateField()
    pflegesatz_enddatum = models.DateField()
    pflegesatz_ferien = models.DecimalField(max_digits=4, decimal_places=2)
    pflegesatz_ferien_startdatum = models.DateField()
    pflegesatz_ferien_enddatum = models.DateField()

    class Meta:
        verbose_name = "Pflegesatz einer Einrichtung"
        verbose_name_plural = "Pflegesätze der Einrichtungen"

    def __str__(self):
        return '{s.name} | {s.pflegesatz} | {s.pflegesatz_ferien}'.format(s=self)


class Ferien(TimeStampedModel):

    name = models.CharField(max_length=100)
    startdatum = models.DateField()
    enddatum = models.DateField()
    einrichtungen = models.ManyToManyField(
        Einrichtung,
        verbose_name='Einrichtungen',
        related_name='ferien'
    )

    class Meta:
        verbose_name = "Ferien"
        verbose_name_plural = "Ferien"

    def __str__(self):
        return self.name


class Schliesstag(TimeStampedModel):

    name = models.CharField(max_length=100)
    datum = models.DateField()
    art = models.CharField(max_length=50)
    einrichtungen = models.ManyToManyField(
        Einrichtung,
        verbose_name='Einrichtungen',
        related_name='schliesstage'
    )

    class Meta:
        verbose_name = "Schliesstag"
        verbose_name_plural = "Schliesstage"

    def __str__(self):
        return '{s.name}: {s.datum}) '.format(s=self)
