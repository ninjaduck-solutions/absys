import datetime

from django.db import models
from django.core.exceptions import ValidationError
from model_utils.models import TimeStampedModel

from absys.apps.schueler.models import Schueler

from . import managers

# TODO: CONSTRAINTS mit clean() (siehe ModelValidation in DjangoDocs) oder Model Field Validatoren umsetzen


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

    def hat_ferien(self, datum):
        """
        Findet heraus, ob an dem Datum ein Ferientag war oder nicht.
        """
        count = self.ferien.filter(
            startdatum__lte=datum,
            enddatum__gte=datum
        ).count()
        return bool(count)

    def get_pflegesatz(self, datum):
        """
        Gibt den Pflegesatz der Einrichtung für das Datum zurück.

        Es exitieren zwei Pflegesätze: Für Schultage und für Ferien.
        """
        pflegesaetze = self.pflegesaetze.get(
            pflegesatz_startdatum__lte=datum,
            pflegesatz_enddatum__gte=datum
        )
        if self.hat_ferien(datum):
            pflegesatz = pflegesaetze.pflegesatz_ferien
        else:
            pflegesatz = pflegesaetze.pflegesatz
        return pflegesatz


class SchuelerInEinrichtung(TimeStampedModel):

    schueler = models.ForeignKey(Schueler, related_name='angemeldet_in_einrichtung')
    einrichtung = models.ForeignKey(Einrichtung, related_name='anmeldungen')
    eintritt = models.DateField("Eintritt")
    austritt = models.DateField("Austritt", help_text="Der Austritt muss nach dem Eintritt erfolgen.")
    sozialamtbescheid_von = models.DateField("Sozialamtbescheid von")
    sozialamtbescheid_bis = models.DateField("Sozialamtbescheid bis",
        help_text="Das Endes des Sozialamtbescheides muss nach dem Beginn erfolgen.")
    pers_pflegesatz = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    pers_pflegesatz_ferien = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    pers_pflegesatz_startdatum = models.DateField(blank=True, null=True)
    pers_pflegesatz_enddatum = models.DateField(blank=True, null=True)

    objects = managers.SchuelerInEinrichtungQuerySet.as_manager()

    class Meta:
        ordering = ("schueler__nachname", "schueler__vorname", "-austritt")
        unique_together = ('schueler', 'einrichtung', 'eintritt', 'austritt')
        verbose_name = "Schueler in der Einrichtung"
        verbose_name_plural = "Schueler in den Einrichtungen"

    def __str__(self):
        return '{s.schueler} in {s.einrichtung} ({s.eintritt} - {s.austritt})'.format(s=self)

    def get_pers_pflegesatz(self, datum):
        """
        Gibt den persönlichen Pflegesatz des Schülers für das Datum zurück.

        Es exitieren zwei Pflegesätze: Für Schultage und für Ferien.
        """
        if self.pers_pflegesatz_startdatum <= datum <= self.pers_pflegesatz_enddatum:
            if self.einrichtung.hat_ferien(datum):
                pflegesatz = self.pers_pflegesatz_ferien
            else:
                pflegesatz = self.pers_pflegesatz
        else:
            pflegesatz = 0.0
        return pflegesatz

    def get_pflegesatz(self, datum):
        """
        Gibt den Pflegesatz für den Schüler in einer Einrichtung für das Datum zurück.

        Es wird der persönliche Pflegesatz des Schülers zurückgegeben. Wenn
        dieser jedoch 0 ist, wird der Einrichtungs-Pflegesatz zurückgegeben.

        Es exitieren zwei Pflegesätze: Für Schultage und für Ferien.
        """
        return self.get_pers_pflegesatz(datum) or self.einrichtung.get_pflegesatz(datum)

    def clean(self):
        if self.eintritt > self.austritt:
            raise ValidationError({'austritt': self._meta.get_field('austritt').help_text})
        if self.sozialamtbescheid_von > self.sozialamtbescheid_bis:
            raise ValidationError(
                {'sozialamtbescheid_bis': self._meta.get_field('sozialamtbescheid_bis').help_text}
            )

    @classmethod
    def get_betreuungstage(cls, startdatum, enddatum):
        """
        Gibt die Liste aller Tage zwischen ``startdatum`` und ``enddatum`` zurück.

        Alle Samstage, Sonntage und Schliesstage werden entfernt.
        """
        schliesstage = tuple(Schliesstag.objects.values_list('datum', flat=True))
        betreuungstage = []
        tag = startdatum
        while tag < enddatum:
            if tag.isoweekday() not in (6, 7) and tag not in schliesstage:
                betreuungstage.append(tag)
            tag += datetime.timedelta(1)
        return betreuungstage


class EinrichtungHatPflegesatz(TimeStampedModel):

    einrichtung = models.ForeignKey(Einrichtung, related_name='pflegesaetze')
    pflegesatz = models.DecimalField(max_digits=4, decimal_places=2)
    pflegesatz_ferien = models.DecimalField(max_digits=4, decimal_places=2)
    pflegesatz_startdatum = models.DateField()
    pflegesatz_enddatum = models.DateField()

    class Meta:
        verbose_name = "Pflegesatz einer Einrichtung"
        verbose_name_plural = "Pflegesätze der Einrichtungen"

    def __str__(self):
        return '{s.einrichtung} | {s.pflegesatz} | {s.pflegesatz_ferien}'.format(s=self)


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

    class Meta:
        verbose_name = "Schliesstag"
        verbose_name_plural = "Schliesstage"

    def __str__(self):
        return '{s.name}: {s.datum}) '.format(s=self)
