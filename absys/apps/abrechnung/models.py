from django.db import IntegrityError, models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from model_utils import Choices
from django.utils.functional import cached_property
from model_utils.models import TimeStampedModel
from django.db.models import Sum

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
    enddatum = models.DateField(
        "Enddatum",
        help_text=("Das Enddatum muss nach dem Startdatum liegen, "
            "darf aber nicht nach dem heutigen Datum liegen."
            " Außerdem müssen Startdatum und Enddatum im gleichen Jahr liegen.")
    )

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

    @cached_property
    def rechnungsbetrag(self):
        return self.rechnungen.aggregate(Sum('summe'))['summe__sum']


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
    max_fehltage = models.PositiveIntegerField("Maximale Fehltage zum Abrechnungstag", default=0)

    objects = managers.RechnungManager.from_queryset(managers.RechnungQuerySet)()

    class Meta:
        ordering = ('-rechnung_sozialamt__startdatum', '-rechnung_sozialamt__enddatum',
            'rechnung_sozialamt', 'schueler')
        unique_together = ('rechnung_sozialamt', 'schueler')
        verbose_name = "Rechnung"
        verbose_name_plural = "Rechnungen"

    def __str__(self):
        msg = "Rechnung {s.nummer} für {s.name_schueler} ({s.rechnung_sozialamt.startdatum} - {s.rechnung_sozialamt.enddatum})"
        return msg.format(s=self)

    @property
    def nummer(self):
        return "R{:06d}".format(self.pk)

    def fehltage_abrechnen(self, schueler_in_einrichtung):
        """
        Nicht abgerechnete Rechnungspositionen pro Schüler seit Eintritt in die Einrichtung abrechnen, bis Limit erreicht.

        Das ``limit`` ist die Anzahl der erlaubten Fehltage minus der bisher abgerechneten Fehltage.
        """
        qs = RechnungsPosition.objects.nicht_abgerechnet(
            schueler_in_einrichtung, self.rechnung_sozialamt.enddatum
        )
        fehltage_abgerechnet = RechnungsPosition.objects.fehltage_abgerechnet(
            schueler_in_einrichtung,
            self.rechnung_sozialamt.enddatum
        ).count()
        limit = schueler_in_einrichtung.fehltage_erlaubt - fehltage_abgerechnet
        if limit < 0:
            limit = 0
        for rechnung_pos in qs[:limit]:
            rechnung_pos.rechnung = self
            if rechnung_pos.rechnung_nicht_abgerechnet == self:
                rechnung_pos.rechnung_nicht_abgerechnet = None
            rechnung_pos.save()

    def abschliessen(self, schueler_in_einrichtung):
        """Instanz für Schüler in Einrichtung aktualisieren (Summe und nicht abgerechnete Fehltage)."""
        self.summe = 0
        if self.positionen.count():
            self.summe = self.positionen.aggregate(models.Sum('pflegesatz'))['pflegesatz__sum']
        self.fehltage_nicht_abgerechnet = RechnungsPosition.objects.nicht_abgerechnet(
            schueler_in_einrichtung,
            self.rechnung_sozialamt.enddatum
        )
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
    noch nicht abgerechnet.
    """

    TAG_ART = Choices(
        ('ferien', "Ferientag"),
        ('schule', "Schultag"),
    )
    sozialamt = models.ForeignKey(Sozialamt, verbose_name="Sozialamt")
    schueler = models.ForeignKey(Schueler, verbose_name="Schüler")
    einrichtung = models.ForeignKey(Einrichtung, verbose_name="Einrichtung")
    rechnung = models.ForeignKey(
        Rechnung,
        verbose_name="Rechnung",
        null=True,
        related_name='positionen'
    )
    rechnung_nicht_abgerechnet = models.ForeignKey(
        Rechnung,
        verbose_name="Rechnung, nicht abgerechnet",
        null=True,
        related_name='fehltage_nicht_abgerechnet'
    )
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

    def clean(self):
        if self.rechnung is not None and self.rechnung_nicht_abgerechnet is not None:
            raise IntegrityError("Die Felder \"Rechnung\" und"
                " \"Rechnung, nicht abgerechnet\" dürfen nicht beide eine Rechnung enthalten.")
