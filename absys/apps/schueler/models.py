from django.db import models
from django.utils.functional import cached_property
from django.utils.timezone import now
from model_utils.models import TimeStampedModel

from . import validators, managers


class Gruppe(TimeStampedModel):

    name = models.CharField(max_length=200, verbose_name="Gruppe")
    bemerkungen = models.TextField(blank=True)

    class Meta:
        verbose_name = "Gruppe"
        verbose_name_plural = "Gruppen"

    def __str__(self):
        return self.name


class Sozialamt(TimeStampedModel):

    name = models.CharField(max_length=35)
    anschrift = models.TextField()
    zahlungspartnernummer = models.CharField(
        "Zahlungspartnernummer",
        max_length=7
    )
    sbkz = models.CharField(
        "Sozialamts-buchungskennzeichen",
        max_length=12,
        blank=True,
    )

    class Meta:
        verbose_name = "Sozialamt"
        verbose_name_plural = "Sozialämter"

    def __str__(self):
        return self.name


class Schueler(TimeStampedModel):

    vorname = models.CharField("Vorname", max_length=30)
    nachname = models.CharField("Nachname", max_length=30)
    geburtsdatum = models.DateField(
        "Geburtsdatum",
        validators=[validators.validate_geburtsdatum_in_vergangenheit]
    )
    bemerkungen = models.TextField(blank=True)
    aktenzeichen = models.CharField("Aktenzeichen", max_length=12, blank=True)
    gruppe = models.ForeignKey(Gruppe, related_name='schueler', on_delete=models.CASCADE)
    sozialamt = models.ForeignKey(Sozialamt, related_name='schueler', on_delete=models.CASCADE)
    inaktiv = models.BooleanField(default=False, help_text=(
        "Schüler können nicht gelöscht, sondern lediglich 'deaktiviert' werden."
        " Dies hat keinerlei Auswirkungen auf die Abrechnung sondern beinflusst"
        " lediglich die Darstellung im Frontend, z.B. Gruppenliste.")
    )
    objects = managers.SchuelerQuerySet.as_manager()

    class Meta:
        ordering = ['nachname', 'vorname']
        verbose_name = "Schüler"
        verbose_name_plural = "Schüler"

    def __str__(self):
        return self.voller_name

    @property
    def voller_name(self):
        return "{s.nachname}, {s.vorname}".format(s=self)

    def get_einrichtung(self, datum):
        """
        Gibt die Einrichtung zum gewählten Datum zurück.
        """
        from absys.apps.einrichtungen.models import Einrichtung
        try:
            einrichtung = self.einrichtungen.get(
                anmeldungen__eintritt__lte=datum,
                anmeldungen__austritt__gte=datum
            )
        except Einrichtung.DoesNotExist:
            einrichtung = None
        return einrichtung

    @cached_property
    def einrichtung(self):
        """
        Gibt die Einrichtung zum aktuellen Zeitpunkt zurück.
        """
        return self.get_einrichtung(now().date())

    def berechne_pflegesatz(self, datum):
        """
        Gibt den Pflegesatz eines Schülers in einer Einrichtung zu dem gegebenen Datum zurück.

        ``SchuelerInEinrichtung.get_pflegesatz()`` berücksichtigt, ob das Datum
        ein Ferien- oder Schultag ist.
        """
        from absys.apps.einrichtungen.models import SchuelerInEinrichtung
        try:
            pflegesatz = self.angemeldet_in_einrichtung.war_angemeldet(datum).get().get_pflegesatz(datum)
        except SchuelerInEinrichtung.DoesNotExist:
            pflegesatz = 0.0
        return pflegesatz
