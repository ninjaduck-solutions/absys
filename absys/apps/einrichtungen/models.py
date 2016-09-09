from django.db import models
from django.core.exceptions import ValidationError
from model_utils.models import TimeStampedModel

from absys.apps.schueler.models import Sozialamt, Schueler

from . import managers

class Standort(TimeStampedModel):

    anschrift = models.TextField()

class Einrichtung(TimeStampedModel):

    name = models.CharField("Name", max_length=30, unique=True)
    kuerzel = models.CharField("Kürzel", max_length=1, unique=True)
    schueler = models.ManyToManyField(
        Schueler,
        verbose_name='Schüler',
        through='SchuelerInEinrichtung',
        related_name='einrichtungen'
    )
    standort = models.ForeignKey(Standort, related_name='einrichtungen')

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
    sozialamt = models.ForeignKey(Sozialamt, related_name='anmeldungen',
        help_text="<span style=\"font-size: 1.3em\">"
            "Es wird automatisch das aktuelle Sozialamt des Schülers ausgewählt.<br><br>"
            "Soll der Schüler in dieser Einrichtung ein neues Sozialamt zugewiesen bekommen"
            ", muss wie folgt vorgegangen werden:<br><br>"
            "1. Das Austrittsdatum des aktuellen Datensatzes auf den letzten Tag für das alte Sozialamt setzen.<br>"
            "2. Das Sozialamt am Datensatz des Schülers ändern.<br>"
            "3. Den Schüler für den neuen Zeitraum der gleichen Einrichtung hinzufügen.<br><br>"
            "</span>")
    eintritt = models.DateField("Eintritt")
    austritt = models.DateField("Austritt", help_text="Der Austritt muss nach dem Eintritt erfolgen.")
    pers_pflegesatz = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    pers_pflegesatz_ferien = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    pers_pflegesatz_startdatum = models.DateField(blank=True, null=True)
    pers_pflegesatz_enddatum = models.DateField(blank=True, null=True)
    fehltage_erlaubt = models.PositiveIntegerField(default=45)

    objects = managers.SchuelerInEinrichtungQuerySet.as_manager()

    class Meta:
        ordering = ("schueler__nachname", "schueler__vorname", "-austritt")
        unique_together = ('schueler', 'einrichtung', 'eintritt', 'austritt')
        verbose_name = "Schüler in Einrichtung"
        verbose_name_plural = "Schüler in Einrichtungen"

    def __str__(self):
        return '{s.schueler} in {s.einrichtung} ({s.eintritt} - {s.austritt})'.format(s=self)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.sozialamt = self.schueler.sozialamt
        super().save(*args, **kwargs)

    def get_pers_pflegesatz(self, datum):
        """
        Gibt den persönlichen Pflegesatz des Schülers für das Datum zurück.

        Es exitieren zwei Pflegesätze: Für Schultage und für Ferien.
        """
        pflegesatz = 0.0
        if self.pers_pflegesatz_startdatum and self.pers_pflegesatz_enddatum:
            if self.pers_pflegesatz_startdatum <= datum <= self.pers_pflegesatz_enddatum:
                if self.einrichtung.hat_ferien(datum):
                    pflegesatz = self.pers_pflegesatz_ferien
                else:
                    pflegesatz = self.pers_pflegesatz
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
        # TODO Zeiträume dürfen sich nicht überlappen
        # Gilt für die Kombination schueler, einrichtung, sozialamt, eintritt, austritt
        # Falls sinnnvoll muss auf django.contrib.postgres.fields.DateRangeField umgestellt werden
        if self.eintritt and self.austritt and self.eintritt > self.austritt:
            raise ValidationError({'austritt': self._meta.get_field('austritt').help_text})

    def war_abwesend(self, tage):
        """Abwesenheitstage für Schüler in Einrichtung im gewählten Zeitraum ermitteln."""
        if len(tage) == 0:
            return self.schueler.anwesenheit.none()
        return self.schueler.anwesenheit.war_abwesend(tage[0], tage[-1]).filter(
            einrichtung=self.einrichtung,
            datum__in=tage
        )


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
    datum = models.DateField(unique=True)
    art = models.CharField(max_length=50)
    einrichtungen = models.ManyToManyField(
        Einrichtung,
        verbose_name='Einrichtungen',
        related_name='schliesstage'
    )

    class Meta:
        verbose_name = "Schließ­tag"
        verbose_name_plural = "Schließ­tage"

    def __str__(self):
        return '{s.name}: {s.datum} '.format(s=self)
