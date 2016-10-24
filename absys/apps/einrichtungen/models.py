import datetime

from django.db import models
from django.core.exceptions import ValidationError
from model_utils.models import TimeStampedModel

from absys.apps.schueler.models import Sozialamt, Schueler

from . import managers


class Standort(TimeStampedModel):

    anschrift = models.TextField()
    konto_iban = models.CharField("IBAN", max_length=22)
    konto_bic = models.CharField("BIC", max_length=12)
    konto_institut = models.CharField("Institut", max_length=100)

    class Meta:
        verbose_name = 'Standort'
        verbose_name_plural = 'Standorte'

    def __str__(self):
        return self.anschrift


class Einrichtung(TimeStampedModel):

    name = models.CharField("Name", max_length=30, unique=True)
    kuerzel = models.CharField("Kürzel", max_length=3, unique=True)
    schueler = models.ManyToManyField(
        Schueler,
        verbose_name='Schüler',
        through='SchuelerInEinrichtung',
        related_name='einrichtungen'
    )
    standort = models.ForeignKey(Standort, related_name='einrichtungen')
    titel = models.IntegerField("Titel", help_text="Darf maximal fünf Ziffern haben.", unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Einrichtung"
        verbose_name_plural = "Einrichtungen"

    def __str__(self):
        return self.name

    def clean(self):
        if self.titel > 100000:
            raise ValidationError({'titel': self._meta.get_field('titel').help_text})

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

        Es existieren zwei Pflegesätze: Für Schultage und für Ferien.
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

    def get_betreuungstage(self, start, ende):
        """Gibt die Betreuungstage für den angegebenen Zeitraum zurück."""
        betreuungstage = []
        schliesstage = self.schliesstage.values_list('datum', flat=True)
        tag = start
        while tag <= ende:
            if tag.isoweekday() not in (6, 7) and tag not in schliesstage:
                betreuungstage.append(tag)
            tag += datetime.timedelta(1)
        return betreuungstage


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
    pers_pflegesatz = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pers_pflegesatz_ferien = models.DecimalField(max_digits=5, decimal_places=2, default=0)
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
        if self.eintritt and self.austritt:
            if self.eintritt > self.austritt:
                raise ValidationError({'austritt': self._meta.get_field('austritt').help_text})
            if not self.pk and self.schueler:
                dubletten = SchuelerInEinrichtung.objects.dubletten(
                    self.schueler, self.eintritt, self.austritt
                ).count()
                if dubletten > 0:
                    msg = (
                        "Für diesen Zeitraum existiert schon eine Anmeldung für {s.schueler}"
                        " für eine Einrichtung."
                    )
                    raise ValidationError(msg.format(s=self))

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
    pflegesatz = models.DecimalField(max_digits=5, decimal_places=2)
    pflegesatz_ferien = models.DecimalField(max_digits=5, decimal_places=2)
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
