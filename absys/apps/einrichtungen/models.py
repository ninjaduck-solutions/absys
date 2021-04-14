import datetime
import decimal

from django.db import models
from django.core.exceptions import ValidationError
from model_utils.models import TimeStampedModel

from absys.apps.schueler.models import Sozialamt, Schueler

from . import configurations, managers, services


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
    EINRICHTUNGS_KONFIGURATIONEN_CHOICES = configurations.choices

    name = models.CharField("Name", max_length=30, unique=True)
    kuerzel = models.CharField("Kürzel", max_length=10, unique=True)
    schueler = models.ManyToManyField(
        Schueler,
        verbose_name='Schüler',
        through='SchuelerInEinrichtung',
        related_name='einrichtungen'
    )
    standort = models.ForeignKey(Standort, related_name='einrichtungen', on_delete=models.CASCADE)
    titel = models.IntegerField("Titel", help_text="Darf maximal fünf Ziffern haben.")
    konfiguration_id = models.IntegerField(
        "Konfiguration",
        choices=EINRICHTUNGS_KONFIGURATIONEN_CHOICES
    )
    pers_bkz= models.BooleanField("Einrichtung mit persönlichen BKZ?",
        default=False)

    class Meta:
        ordering = ['name']
        verbose_name = "Einrichtung"
        verbose_name_plural = "Einrichtungen"

    def __str__(self):
        return self.name

    def clean(self):
        if self.titel and self.titel > 100000:
            raise ValidationError(
                {'titel': self._meta.get_field('titel').help_text},
                code='title_zu_lang'
            )
        if self.pk and self.pers_bkz:
            for schueler in self.schueler.all():
                if schueler and not schueler.aktenzeichen:
                    msg = (
                        "Es existieren Schüler in dieser Einrichtung, "
                        "die noch kein Aktenzeichen besitzen. "
                        "Eine Einrichtung , die persönlichen Buchungskennzeichen verwendet, "
                        "darf nur Schüler beinhalten, für die ein Aktenzeichen eingtragen ist."
                    )
                    raise ValidationError(msg)


    def hat_ferien(self, datum):
        """
        Findet heraus, ob an dem Datum ein Ferientag war oder nicht.
        """
        ferien = self.ferien.filter(
            startdatum__lte=datum,
            enddatum__gte=datum
        )
        # In diesem Fall ist die Nutzung von len() schneller als die von
        # QuerySet.count().
        return bool(len(ferien))

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
            fester_schliesstag = tag.isoweekday() in self.konfiguration.feste_schliesstage
            if not fester_schliesstag and tag not in schliesstage:
                betreuungstage.append(tag)
            tag += datetime.timedelta(1)
        return betreuungstage

    @property
    def konfiguration(self):
        return configurations.registry[self.konfiguration_id]


class SchuelerInEinrichtung(TimeStampedModel):

    BARGELD_VOLLER_SATZ = 12
    ANTEILE_BARGELD_CHOICES = (
        (0, "0 (keine Auszahlung)"),
    ) + tuple([(i, str(i)) for i in range(1, 12)]) + (
        (BARGELD_VOLLER_SATZ, "12 (voller Satz)"),
    )

    schueler = models.ForeignKey(Schueler, related_name='angemeldet_in_einrichtung', on_delete=models.CASCADE)
    einrichtung = models.ForeignKey(Einrichtung, related_name='anmeldungen', on_delete=models.CASCADE)
    sozialamt = models.ForeignKey(
        Sozialamt,
        related_name='anmeldungen',
        on_delete=models.CASCADE,
        help_text=
        "<span style=\"font-size: 1.3em\">"
        "Es wird automatisch das aktuelle Sozialamt des Schülers ausgewählt.<br><br>"
        "Soll der Schüler in dieser Einrichtung ein neues Sozialamt zugewiesen bekommen"
        ", muss wie folgt vorgegangen werden:<br><br>"
        "1. Das Austrittsdatum des aktuellen Datensatzes auf den letzten Tag für das alte Sozialamt setzen.<br>"
        "2. Das Sozialamt am Datensatz des Schülers ändern.<br>"
        "3. Einen neuen Schüler-in-Einrichtung-Datensatz für den neuen Zeitraum für den gleichen Schüler der gleichen Einrichtung hinzufügen.<br><br>"
        "</span>"
    )
    eintritt = models.DateField("Eintritt")
    austritt = models.DateField("Austritt", help_text="Der Austritt muss nach dem Eintritt erfolgen.")
    pers_pflegesatz = models.DecimalField(
        "Persönlicher Pflegesatz",
        help_text=
        "Wenn der Schüler keinen persönlichen Pflegesatz zugewiesen bekommen hat, "
        "muss in diesem Feld '0' stehen bleiben.",
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    pers_pflegesatz_ferien = models.DecimalField(
        "Persönlicher Pflegesatz Ferien",
        help_text=
        "Wenn der Schüler keinen persönlichen Pflegesatz für Ferien zugewiesen bekommen hat, "
        "muss in diesem Feld '0' stehen bleiben.",
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    pers_pflegesatz_startdatum = models.DateField(
        "Startdatum persönlicher Pflegesatz",
        blank=True,
        null=True,
    )
    pers_pflegesatz_enddatum = models.DateField(
        "Enddatum persönlicher Pflegesatz",
        blank=True,
        null=True,
    )
    fehltage_erlaubt = models.PositiveIntegerField(null=False, blank=False)
    anteile_bargeld = models.IntegerField(
        "Anteile Bargeld",
        choices=ANTEILE_BARGELD_CHOICES,
        default=BARGELD_VOLLER_SATZ,
    )

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

    @property
    def fehltage_berechnet(self):
        return services.get_billable_missing_days(self.eintritt, self.austritt)

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
        if not self.schueler.aktenzeichen and self.einrichtung.pers_bkz:
            msg = (
                "Dieser Schüler soll einer Einrichtung mit persönlichen Buchungskennzeichen hinzugefügt werden."
                " Bitte vergeben Sie für diesen Schüler zuerst ein Aktenzeichen,"
                " das als persönliches Buchungskennzeichen genutzt werden kann."
            )
            raise ValidationError(msg)
        if self.eintritt and self.austritt:
            if self.eintritt > self.austritt:
                raise ValidationError(
                    {'austritt': self._meta.get_field('austritt').help_text},
                    code='austritt_vor_eintritt'
                )
            if not self.pk and self.schueler:
                dubletten = SchuelerInEinrichtung.objects.dubletten(
                    self.schueler, self.eintritt, self.austritt
                ).count()
                if dubletten > 0:
                    msg = (
                        "Für diesen Zeitraum existiert schon eine Anmeldung für {s.schueler}"
                        " für eine Einrichtung."
                    )
                    raise ValidationError(msg.format(s=self), code='anmeldung_existiert_schon')

    def war_abwesend(self, tage):
        """Abwesenheitstage für Schüler in Einrichtung im gewählten Zeitraum ermitteln."""
        if len(tage) == 0:
            return self.schueler.anwesenheit.none()
        return self.schueler.anwesenheit.war_abwesend(tage[0], tage[-1]).filter(datum__in=tage)

    def bargeldbetrag(self, startdatum, enddatum):
        """
        Berechnung den Bargeldbetrag an einem bestimmten Datum.

        - Für jeden Schüler wird ist ein Bargeldsatz-Anteil definiert (0-12),
          denn zur Berechnung des Bargeldsatz-Anteils wird folgende Formel
          verwendet: ``Bargeldsatz * Anteil / 12``
        - Da das Enddatum einer Rechnung frei definiert werden kann, muss der
          Bargeldsatz anteilig berechnet werden:
          ``Bargeldsatz-Anteil / Tage im Monat * Tage im Abrechnungszeitraum für diesen Monat``,
          danach Runden auf zwei Stellen
        """
        bargeldbetrag = decimal.Decimal()
        if self.einrichtung.konfiguration.bargeldauszahlung:
            bargeldsatz = Bargeldsatz.objects.nach_lebensalter(enddatum, self.schueler.geburtsdatum)
            if bargeldsatz is not None:
                bargeldanteil = bargeldsatz.betrag * self.anteile_bargeld / self.BARGELD_VOLLER_SATZ
                bargeldbetrag = services.bargeld_zeitraum(bargeldanteil, startdatum, enddatum)
        return bargeldbetrag


class EinrichtungHatPflegesatz(TimeStampedModel):

    einrichtung = models.ForeignKey(Einrichtung, related_name='pflegesaetze', on_delete=models.CASCADE)
    pflegesatz = models.DecimalField("Pflegesatz", max_digits=5, decimal_places=2)
    pflegesatz_ferien = models.DecimalField("Pflegesatz Ferien", max_digits=5, decimal_places=2)
    pflegesatz_startdatum = models.DateField("Startdatum")
    pflegesatz_enddatum = models.DateField("Enddatum")

    objects = managers.EinrichtungHatPflegesatzQuerySet.as_manager()

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

    objects = managers.FerienQuerySet.as_manager()

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


class Bettengeldsatz(TimeStampedModel):

    einrichtung = models.ForeignKey(
        Einrichtung,
        verbose_name="Einrichtung",
        related_name='bettengeldsaetze',
        on_delete=models.CASCADE
    )
    startdatum = models.DateField("Startdatum")
    enddatum = models.DateField(
        "Enddatum",
        help_text="Das Enddatum muss nach dem Startdatum liegen."
    )
    satz = models.DecimalField(
        "Satz", max_digits=8, decimal_places=2,
        help_text=(
            "<p>Dieses ist Feld ist doppelt belegt:<br><ol>"
            "<li>Für 280-Tages-Einrichtungen ist dieses Feld der Abwesenheitsvergütungssatz.</li>"
            "<li>Für 365-Tages-Einrichtungen ist dieses Feld der Bettengeldsatz.</li>"
            "<ol></p>"
        )
    )

    objects = managers.BettengeldsatzQuerySet.as_manager()

    class Meta:
        unique_together = ('einrichtung', 'startdatum', 'enddatum')
        verbose_name = "Bettengeldsatz"
        verbose_name_plural = "Bettengeldsätze"

    def __str__(self):
        return "Bettengeldsatz {s.satz} € für {s.einrichtung}".format(s=self)

    def clean(self):
        if self.startdatum and self.enddatum and self.startdatum > self.enddatum:
            raise ValidationError(
                {'enddatum': "Das Enddatum muss nach dem Startdatum liegen."},
                code='enddatum_nach_startdatum'
            )


class Bargeldsatz(TimeStampedModel):
    """
    Bargeldsatz pro Monat.

    Wird nur an Schüler ausgezahlt, deren Einrichtung einen Bargeldsatz
    auszahlt.
    """

    LEBENSJAHR_CHOICES = (
        (3, "3. Lebensjahr"),
    ) + tuple([(i, "{:d}. Lebensjahr".format(i)) for i in range(4, 18)]) + (
        (18, "18. Lebensjahr"),
    )

    lebensjahr = models.IntegerField(
        "Lebensjahr", choices=LEBENSJAHR_CHOICES, unique=True
    )
    betrag = models.DecimalField("Betrag pro Monat", max_digits=5, decimal_places=2)

    objects = managers.BargeldsatzManager()

    class Meta:
        verbose_name = "Bargeldsatz"
        verbose_name_plural = "Bargeldsätze"

    def __str__(self):
        return "{s.lebensjahr}. Lebensjahr: {s.betrag} €".format(s=self)
