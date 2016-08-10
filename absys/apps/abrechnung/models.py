from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from model_utils import Choices
from model_utils.models import TimeStampedModel

from absys.apps.einrichtungen.models import Einrichtung
from absys.apps.schueler.models import Schueler, Sozialamt

from . import managers


class RechnungSozialamt(TimeStampedModel):
    """
    Eine Sozialamtsrechnung fasst mehrere Rechnungen zusammen.

    - Sozialamt (Fremdschlüssel)
    - Sozialamt Anschrift
    - Startdatum
    - Enddatum
    """

    sozialamt = models.ForeignKey(Sozialamt, verbose_name="Sozialamt", related_name='rechnungen')
    sozialamt_anschrift = models.TextField()
    startdatum = models.DateField("Startdatum")
    enddatum = models.DateField("Enddatum",
        help_text=("Das Enddatum muss nach dem Startdatum liegen, ",
            "darf aber nicht nach dem heutigen Datum liegen.",
            " Außerdem müssen Startdatum und Enddatum im gleichen Jahr liegen."))

    objects = managers.RechnungSozialamtManager()

    class Meta:
        ordering = ('-startdatum', '-enddatum', 'sozialamt')
        unique_together = ('sozialamt', 'startdatum', 'enddatum')
        verbose_name = "Sozialamtsrechnung"
        verbose_name_plural = "Sozialamtsrechnungen"

    def __str__(self):
        msg = "Sozialamtsrechnung {s.nummer} für {s.sozialamt} ({s.startdatum} - {s.enddatum})"
        return msg.format(s=self)

    def clean(self):
        if self.startdatum > self.enddatum:
            raise ValidationError({'enddatum': "Das Enddatum muss nach dem Startdatum liegen."})
        if self.enddatum > now().date():
            raise ValidationError(
                {'enddatum': "Das Enddatum darf nicht nach dem heutigen Datum liegen."}
            )
        if self.startdatum.year != self.enddatum.year:
            raise ValidationError(
                {'enddatum': "Startdatum und Enddatum müssen im gleichen Jahr liegen."}
            )
        qs = RechnungSozialamt.objects.filter(
            models.Q(
                models.Q(startdatum__range=(self.startdatum, self.enddatum)) |
                models.Q(enddatum__range=(self.startdatum, self.enddatum))
            ) |
            models.Q(startdatum__lte=self.startdatum, enddatum__gte=self.enddatum),
            sozialamt=self.sozialamt
        )
        if qs.count():
            raise ValidationError(
                {'startdatum': "Für den ausgewählten Zeitraum existiert schon eine Rechnung."}
            )

    @property
    def nummer(self):
        return "S{:06d}".format(self.pk)


class Rechnung(TimeStampedModel):
    """
    Metadaten einer Rechnung für einen Schüler in einem bestimmten Zeitraum.

    Pro Model-Instanz eindeutig:

    - Schüler (Fremdschlüssel)

    Die folgenden Felder werden beim Erstellen oder Abschluss der Rechnung
    befüllt und können nicht mehr verändert werden. Es sind keine
    Fremdschlüssel.

    - Name des Schülers (Erstellung)
    - Rechnungssumme (Abschluss)
    - Fehltage im Abrechnungszeitraum (Erstellung)
    - Fehltage seit Eintritt in die Einrichtung (Erstellung)
    - Bisher nicht abgerechnete Fehltage (Abschluss)
    - Maximale Fehltage zum Abrechnungstag (Erstellung)
    """

    rechnung_sozialamt = models.ForeignKey(RechnungSozialamt, verbose_name="Sozialamtsrechnung",
        related_name='rechnungen')
    schueler = models.ForeignKey(Schueler, verbose_name="Schüler", related_name='rechnungen')
    name_schueler = models.CharField("Name des Schülers", max_length=61)
    summe = models.DecimalField("Gesamtbetrag", max_digits=7, decimal_places=2, null=True)
    fehltage = models.PositiveIntegerField("Fehltage im Abrechnungszeitraum", default=0)
    fehltage_gesamt = models.PositiveIntegerField("Fehltage seit Eintritt in die Einrichtung", default=0)
    fehltage_nicht_abgerechnet = models.PositiveIntegerField("Bisher nicht abgerechnete Fehltage", default=0)
    max_fehltage = models.PositiveIntegerField("Maximale Fehltage zum Abrechnungstag", default=0)

    objects = managers.RechnungManager()

    class Meta:
        ordering = ('-rechnung_sozialamt__startdatum', '-rechnung_sozialamt__enddatum',
            'rechnung_sozialamt', 'schueler')
        unique_together = ('rechnung_sozialamt', 'schueler')
        verbose_name = "Rechnung"
        verbose_name_plural = "Rechnungen"

    def __str__(self):
        msg = "Rechnung {s.nummer} für {s.name_schueler} ({s.startdatum} - {s.enddatum})"
        return msg.format(s=self)

    @property
    def nummer(self):
        return "R{:06d}".format(self.pk)

    def fehltage_abrechnen(self, schueler_in_einrichtung):
        """
        Nicht abgerechnete Rechnungspositionen pro Schüler seit Eintritt in die Einrichtung abrechnen, bis Limit erreicht.
        """
        qs = RechnungsPosition.objects.nicht_abgerechnet(
            schueler_in_einrichtung, self.rechnung_sozialamt.enddatum
        )
        limit = (
            schueler_in_einrichtung.fehltage_erlaubt -
            schueler_in_einrichtung.schueler.rechnungen.letzte_rechnung_fehltage_gesamt(
                self.rechnung_sozialamt.enddatum.year
            )
        )
        for rechnung_pos in qs[:limit]:
            rechnung_pos.rechnung = self
            rechnung_pos.save()

    def abschliessen(self, schueler_in_einrichtung):
        """Instanz für Schüler in Einrichtung aktualisieren (Summe und nicht abgerechnete Fehltage)."""
        self.summe = self.positionen.aggregate(models.Sum('pflegesatz'))['pflegesatz__sum']
        self.fehltage_nicht_abgerechnet = RechnungsPosition.objects.nicht_abgerechnet(
            schueler_in_einrichtung,
            self.rechnung_sozialamt.enddatum
        ).count()
        self.save()


class RechnungsPosition(TimeStampedModel):
    """
    Daten einer Rechnungsposition für einen Schüler an einem bestimmten Datum.

    Jede Rechnungsposition hat folgende Felder:

    - Sozialamt (Fremdschlüssel)
    - Schüler (Fremdschlüssel)
    - Einrichtung (Fremdschlüssel)
    - Rechnung (Fremdschlüssel oder None)
    - Datum
    - Einrichtung (String)
    - Schul- oder Ferientag
    - Abwesenheit
    - Pflegesatz

    Wenn der Wert von Rechnung ``None`` ist, wurde die ``RechnungsPosition``
    noch nicht abgerechnet,
    """

    TAG_ART = Choices(
        ('ferien', "Ferientag"),
        ('schule', "Schultag"),
    )
    sozialamt = models.ForeignKey(Sozialamt, verbose_name="Sozialamt")
    schueler = models.ForeignKey(Schueler, verbose_name="Schüler")
    einrichtung = models.ForeignKey(Einrichtung, verbose_name="Schüler")
    rechnung = models.ForeignKey(Rechnung, verbose_name="Rechnung", null=True,
        related_name='positionen')
    datum = models.DateField("Datum")
    name_einrichtung = models.CharField("Einrichtung", max_length=20)
    tag_art = models.CharField("Schul- oder Ferientag", choices=TAG_ART, default=TAG_ART.schule, max_length=20)
    abwesend = models.BooleanField("Abwesenheit", default=False)
    pflegesatz = models.DecimalField("Pflegesatz", max_digits=4, decimal_places=2)

    objects = managers.RechnungsPositionManager.from_queryset(managers.RechnungsPositionQuerySet)()

    class Meta:
        ordering = ('sozialamt', 'schueler', 'einrichtung', 'datum')
        unique_together = ('schueler', 'datum')
        verbose_name = "Rechnungsposition"
        verbose_name_plural = "Rechnungspositionen"

    def __str__(self):
        return "Rechnungsposition für {s.schueler.voller_name} am {s.datum}".format(s=self)
