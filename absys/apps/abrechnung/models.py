from django.db import models
from django.core.exceptions import ValidationError
from model_utils import Choices
from model_utils.models import TimeStampedModel

from absys.apps.einrichtungen.models import Einrichtung
from absys.apps.schueler.models import Schueler, Sozialamt

from . import managers


class Rechnung(TimeStampedModel):
    """
    Metadaten einer Rechnung für einen Schüler in einem bestimmten Zeitraum.

    Die folgenden Felder sind pro Model-Instanz eindeutig:

    - Sozialamt (Fremdschlüssel)
    - Schüler (Fremdschlüssel)
    - Startdatum
    - Enddatum

    Es kann nur das Sozialamt nachträglich geändert werden.

    Die anderen Felder werden beim Erstellen der Rechnung befüllt und können
    nicht mehr verändert werden. Es sind keine Fremdschlüssel.

    - Name des Schülers
    - Rechnungssumme
    - Fehltage im Abrechnungszeitraum
    - Fehltage seit Eintritt in die Einrichtung
    - Bisher nicht abgerechnete Fehltage
    - Maximale Fehltage zum Abrechnungstag
    """

    sozialamt = models.ForeignKey(Sozialamt, verbose_name="Sozialamt")
    schueler = models.ForeignKey(Schueler, verbose_name="Schüler")
    startdatum = models.DateField("Startdatum")
    enddatum = models.DateField("Enddatum",
        help_text="Das Enddatum muss nach dem Startdatum liegen.")
    name_schueler = models.CharField("Name des Schülers", max_length=61)
    summe = models.DecimalField("Gesamtbetrag", max_digits=7, decimal_places=2, null=True)
    fehltage = models.PositiveIntegerField("Fehltage im Abrechnungszeitraum", default=0)
    fehltage_jahr = models.PositiveIntegerField("Fehltage seit Eintritt in die Einrichtung", default=0)
    fehltage_nicht_abgerechnet = models.PositiveIntegerField("Bisher nicht abgerechnete Fehltage", default=0)
    max_fehltage = models.PositiveIntegerField("Maximale Fehltage zum Abrechnungstag", default=0)

    objects = managers.RechnungManager()

    class Meta:
        ordering = ('sozialamt', 'schueler', 'startdatum', 'enddatum')
        unique_together = ('sozialamt', 'schueler', 'startdatum', 'enddatum')
        verbose_name = "Rechnung"
        verbose_name_plural = "Rechnungen"

    def __str__(self):
        msg = "Rechnung {s.nummer} Für {s.name_schueler} ({s.startdatum} - {s.enddatum})"
        return msg.format(s=self)

    def clean(self):
        if self.startdatum > self.enddatum:
            raise ValidationError({'enddatum': self._meta.get_field('enddatum').help_text})
        qs = Rechnung.objects.filter(
            models.Q(
                models.Q(startdatum__range=(self.startdatum, self.enddatum)) |
                models.Q(enddatum__range=(self.startdatum, self.enddatum))
            ) |
            models.Q(startdatum__lte=self.startdatum, enddatum__gte=self.enddatum),
            sozialamt=self.sozialamt,
            schueler=self.schueler
        )
        if qs.count():
            raise ValidationError(
                {'startdatum': "Für den ausgewählten Zeitraum existiert schon eine Rechnung."}
            )

    @property
    def nummer(self):
        return "{:06d}".format(self.pk)

    def fehlltage_abrechnen(self, schueler_in_einrichtung):
        """
        Nicht abgerechnete Instanzen pro Schüler seit Eintritt in die Einrichtung abrechnen, bis Limit erreicht.
        """
        # TODO Abrechnung fertig stellen
        qs = RechnungsPosition.objects.nicht_abgerechnet(schueler_in_einrichtung, self.enddatum)
        limit = schueler_in_einrichtung.fehltage - 0
        for rechnung_pos in qs[:limit]:
            rechnung_pos.rechnung = self
            rechnung_pos.save()

    def abschliessen(self, schueler_in_einrichtung):
        """Instanz für Schüler in Einrichtung aktualisieren (Summe und Fehltage)."""
        pass


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

    objects = managers.RechnungsPositionManager()

    class Meta:
        ordering = ('sozialamt', 'schueler', 'einrichtung', 'datum')
        unique_together = ('schueler', 'datum')
        verbose_name = "Rechnungsposition"
        verbose_name_plural = "Rechnungspositionen"

    def __str__(self):
        return "Rechnungsposition für {s.schueler.voller_name} am {s.datum}".format(s=self)
