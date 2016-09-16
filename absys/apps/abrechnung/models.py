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
        return self.rechnungen_schueler.aggregate(Sum('summe'))['summe__sum']


class RechnungSchueler(TimeStampedModel):
    """
    Metadaten einer Rechnung für einen Schüler in einem bestimmten Zeitraum.

    Pro Model-Instanz zusammen eindeutig:

    - Sozialamtsrechnung (Fremdschlüssel)
    - Schüler (Fremdschlüssel)

    Die folgenden Felder werden beim Erstellen oder Abschluss der Rechnung
    befüllt und können nicht mehr verändert werden. Es sind keine
    Fremdschlüssel.

    - Name des Schülers (Erstellung)
    - Rechnungssumme (Abschluss)
    - Fehltage im Abrechnungszeitraum (Erstellung)
    - Bisher nicht abgerechnete Fehltage (Abschluss)
    """

    rechnung_sozialamt = models.ForeignKey(RechnungSozialamt, verbose_name="Sozialamtsrechnung",
        related_name='rechnungen_schueler')
    schueler = models.ForeignKey(Schueler, verbose_name="Schüler", related_name='rechnungen_schueler')
    name_schueler = models.CharField("Name des Schülers", max_length=61)
    summe = models.DecimalField("Gesamtbetrag", max_digits=8, decimal_places=2, null=True)
    fehltage = models.PositiveIntegerField("Fehltage im Abrechnungszeitraum", default=0)

    objects = managers.RechnungSchuelerManager()

    class Meta:
        ordering = ('-rechnung_sozialamt__startdatum', '-rechnung_sozialamt__enddatum',
            'rechnung_sozialamt', 'schueler')
        unique_together = ('rechnung_sozialamt', 'schueler')
        verbose_name = "Schüler-Rechnung"
        verbose_name_plural = "Schüler-Rechnungen"

    def __str__(self):
        msg = "Schüler-Rechnung {s.nummer} für {s.name_schueler} ({s.rechnung_sozialamt.startdatum} - {s.rechnung_sozialamt.enddatum})"
        return msg.format(s=self)

    @property
    def nummer(self):
        return "SR{:06d}".format(self.pk)

    def fehltage_abrechnen(self, schueler_in_einrichtung):
        """
        Nicht abgerechnete Rechnungspositionen pro Schüler seit Eintritt in die Einrichtung abrechnen, bis Limit erreicht.

        Das ``limit`` ist die Anzahl der erlaubten Fehltage minus der bisher abgerechneten Fehltage.
        """
        qs = RechnungsPositionSchueler.objects.nicht_abgerechnet(
            schueler_in_einrichtung, self.rechnung_sozialamt.enddatum
        )
        fehltage_abgerechnet = RechnungsPositionSchueler.objects.fehltage_abgerechnet(
            schueler_in_einrichtung,
            self.rechnung_sozialamt.enddatum
        ).count()
        limit = schueler_in_einrichtung.fehltage_erlaubt - fehltage_abgerechnet
        if limit < 0:
            limit = 0
        for rechnung_pos in qs[:limit]:
            rechnung_pos.rechnung_schueler = self
            if rechnung_pos.rechnung_nicht_abgerechnet == self:
                rechnung_pos.rechnung_nicht_abgerechnet = None
            rechnung_pos.save()

    def abschliessen(self, schueler_in_einrichtung):
        """Instanz für Schüler in Einrichtung aktualisieren (Summe und nicht abgerechnete Fehltage)."""
        self.summe = 0
        if self.positionen.count():
            self.summe = self.positionen.aggregate(models.Sum('pflegesatz'))['pflegesatz__sum']
        nicht_abgerechnet = RechnungsPositionSchueler.objects.nicht_abgerechnet(
            schueler_in_einrichtung,
            self.rechnung_sozialamt.enddatum
        )
        if nicht_abgerechnet.count():
            self.fehltage_nicht_abgerechnet.add(*nicht_abgerechnet)
        self.save()


class RechnungsPositionSchueler(TimeStampedModel):
    """
    Daten einer Rechnungsposition für einen Schüler an einem bestimmten Datum.

    Jede Rechnungsposition hat folgende Felder:

    - Sozialamt (Fremdschlüssel)
    - Schüler (Fremdschlüssel)
    - Einrichtung (Fremdschlüssel)
    - Schüler-Rechnung (Fremdschlüssel oder None)
    - Datum
    - Einrichtung (String)
    - Schul- oder Ferientag
    - Abwesenheit
    - Pflegesatz

    Wenn der Wert von Rechnung ``None`` ist, wurde die ``RechnungsPositionSchueler``
    noch nicht abgerechnet.
    """

    TAG_ART = Choices(
        ('ferien', "Ferientag"),
        ('schule', "Schultag"),
    )
    sozialamt = models.ForeignKey(Sozialamt, verbose_name="Sozialamt")
    schueler = models.ForeignKey(Schueler, verbose_name="Schüler")
    einrichtung = models.ForeignKey(Einrichtung, verbose_name="Einrichtung")
    rechnung_schueler = models.ForeignKey(
        RechnungSchueler,
        verbose_name="Schüler-Rechnung",
        null=True,
        related_name='positionen'
    )
    rechnung_nicht_abgerechnet = models.ForeignKey(
        RechnungSchueler,
        verbose_name="Schüler-Rechnung, nicht abgerechnet",
        null=True,
        related_name='fehltage_nicht_abgerechnet'
    )
    datum = models.DateField("Datum")
    name_einrichtung = models.CharField("Einrichtung", max_length=20)
    tag_art = models.CharField("Schul- oder Ferientag", choices=TAG_ART, default=TAG_ART.schule, max_length=20)
    abwesend = models.BooleanField("Abwesenheit", default=False)
    pflegesatz = models.DecimalField("Pflegesatz", max_digits=5, decimal_places=2)

    objects = managers.RechnungsPositionSchuelerManager.from_queryset(managers.RechnungsPositionSchuelerQuerySet)()

    class Meta:
        ordering = ('sozialamt', 'schueler', 'einrichtung', 'datum')
        unique_together = ('schueler', 'datum')
        verbose_name = "Schüler-Rechnungsposition"
        verbose_name_plural = "Schüler-Rechnungspositionen"

    def __str__(self):
        return "Schüler-Rechnungsposition für {s.schueler.voller_name} am {s.datum}".format(s=self)

    def clean(self):
        if self.rechnung_schueler is not None and self.rechnung_nicht_abgerechnet is not None:
            raise IntegrityError("Die Felder \"Schüler-Rechnung\" und"
                " \"Schüler-Rechnung, nicht abgerechnet\" dürfen nicht beide eine Schüler-Rechnung enthalten.")


class RechnungEinrichtung(TimeStampedModel):
    """
    Metadaten einer Rechnung für eine Einrichtung in einem bestimmten Zeitraum.

    Pro Model-Instanz zusammen eindeutig:

    - Sozialamtsrechnung (Fremdschlüssel)
    - Einrichtung (Fremdschlüssel)

    Die folgenden Felder werden beim Erstellen oder Abschluss der Rechnung
    befüllt und können nicht mehr verändert werden. Es sind keine
    Fremdschlüssel.

    - Name der Einrichtung (Erstellung)
    - Buchungskennzeichen (Erstellung)
    - Fälligkeitsdatum (Erstellung)
    - Betreuungstage (Erstellung)
    - Rechnungssumme (Abschluss)
    """

    rechnung_sozialamt = models.ForeignKey(RechnungSozialamt, verbose_name="Sozialamtsrechnung",
        related_name='rechnungen_einrichtungen')
    einrichtung = models.ForeignKey(Einrichtung, verbose_name="Einrichtung", related_name='rechnungen')
    name_einrichtung = models.CharField("Name der Einrichtung", max_length=30)
    buchungskennzeichen = models.CharField("Buchungskennzeichen", max_length=20)
    datum_faellig = models.DateField("Fälligkeitsdatum")
    betreuungstage = models.PositiveIntegerField(default=0)
    summe = models.DecimalField("Gesamtbetrag", max_digits=8, decimal_places=2, null=True)

    objects = managers.RechnungEinrichtungManager()

    class Meta:
        ordering = ('-rechnung_sozialamt__startdatum', '-rechnung_sozialamt__enddatum',
            'rechnung_sozialamt', 'einrichtung')
        unique_together = ('rechnung_sozialamt', 'einrichtung')
        verbose_name = "Einrichtungs-Rechnung"
        verbose_name_plural = "Einrichtungs-Rechnungen"

    def __str__(self):
        msg = (
            "Einrichtungs-Rechnung {s.nummer} für {s.name_einrichtung}"
            " ({s.rechnung_sozialamt.startdatum} - {s.rechnung_sozialamt.enddatum})"
        )
        return msg.format(s=self)

    @property
    def nummer(self):
        return "ER{:06d}".format(self.pk)

    def abrechnen(self, schueler):
        return self.positionen.create(
            schueler=schueler,
            fehltage_max=0,
            anwesend=0,
            fehltage=0,
            fehltage_uebertrag=0,
            fehltage_gesamt=0,
            fehltage_abrechnung=0,
            zahltage=0,
            summe=0
        )

    def abschliessen(self):
        """Rechnung abschließen."""
        self.summe = 0
        if self.positionen.count():
            self.summe = self.positionen.aggregate(models.Sum('summe'))['summe__sum']
        self.save()


class RechnungsPositionEinrichtung(TimeStampedModel):
    """
    Daten einer Rechnungsposition für einen Schüler in einer Einrichtung in einem bestimmten Zeitraum.

    Jede Rechnungsposition hat folgende Felder:

    - Schüler (Fremdschlüssel)
    - Einrichtungs-Rechnung (Fremdschlüssel)
    - Maximale Fehltage
    - Anwesend
    - Fehltage
    - Übertrag Fehltage ab 1.1. des laufenden Jahres oder Eintritt
    - Fehltage gesamt
    - Fehltage zur Abrechnung im Abrechnungszeitraum
    - Zahltage im Abrechnungszeitraum (Anwesend + Fehltage zur Abrechnung im Abrechnungszeitraum)
    - Summe der Aufwendungen
    """

    schueler = models.ForeignKey(Schueler, verbose_name="Schüler")
    name_schueler = models.CharField("Name des Schülers", max_length=61)
    rechnung_einrichtung = models.ForeignKey(
        RechnungEinrichtung,
        verbose_name="Einrichtungs-Rechnung",
        related_name='positionen'
    )
    fehltage_max = models.PositiveIntegerField("Maximale Fehltage")
    anwesend = models.PositiveIntegerField("Anwesend")
    fehltage = models.PositiveIntegerField("Fehltage")
    fehltage_uebertrag = models.PositiveIntegerField("Übertrag Fehltage ab 1.1. des laufenden Jahres oder Eintritt")
    fehltage_gesamt = models.PositiveIntegerField("Fehltage gesamt")
    fehltage_abrechnung = models.PositiveIntegerField("Fehltage zur Abrechnung im Abrechnungszeitraum")
    zahltage = models.PositiveIntegerField("Zahltage im Abrechnungszeitraum")
    summe = models.DecimalField("Summe der Aufwendungen", max_digits=8, decimal_places=2,
        null=True)

    class Meta:
        ordering = (
            'schueler',
            'rechnung_einrichtung',
            'rechnung_einrichtung__rechnung_sozialamt__startdatum'
        )
        unique_together = ('schueler', 'rechnung_einrichtung')
        verbose_name = "Einrichtungs-Rechnungsposition"
        verbose_name_plural = "Einrichtungs-Rechnungspositionen"

    def __str__(self):
        msg = (
            "Einrichtungs-Rechnungsposition für {s.name_schueler}"
            " in {s.rechnung_einrichtung.name_einrichtung}"
            " ({s.rechnung_einrichtung.rechnung_sozialamt.startdatum}"
            " - {s.rechnung_einrichtung.rechnung_sozialamt.enddatum})"
        )
        return msg.format(s=self)

    @cached_property
    def detailabrechnung(self):
        return self.schueler.rechnungspositionschueler_set.filter(
            datum__range=(
                self.rechnung_einrichtung.rechnung_sozialamt.startdatum,
                self.rechnung_einrichtung.rechnung_sozialamt.enddatum
            )
        )
