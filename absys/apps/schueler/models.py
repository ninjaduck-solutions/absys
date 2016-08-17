from django.db import models
from django.utils.functional import cached_property
from django.utils.timezone import now
from model_utils.models import TimeStampedModel

# TODO: CONSTRAINTS mit clean() (siehe ModelValidation in DjangoDocs) oder Model Field Validatoren umsetzen
# TODO: Schueler kann inaktiv gesetzt werden -> Datensätze bleiben erhalten, wird aber nicht mehr berücksichtigt


class Gruppe(TimeStampedModel):

    name = models.CharField(max_length=200)
    bemerkungen = models.TextField(blank=True)

    class Meta:
        verbose_name = "Gruppe"
        verbose_name_plural = "Gruppen"

    def __str__(self):
        return self.name


class Stufe(TimeStampedModel):

    name = models.CharField(max_length=200)
    bemerkungen = models.TextField(blank=True)

    class Meta:
        verbose_name = "Stufe"
        verbose_name_plural = "Stufen"

    def __str__(self):
        return self.name


class Sozialamt(TimeStampedModel):

    name = models.CharField(max_length=200)
    anschrift = models.TextField()
    konto_iban = models.CharField(max_length=22)
    konto_institut = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Sozialamt"
        verbose_name_plural = "Sozialämter"

    def __str__(self):
        return self.name


class Schueler(TimeStampedModel):

    vorname = models.CharField("Vorname", max_length=30)
    nachname = models.CharField("Nachname", max_length=30)
    geburtsdatum = models.DateField()
    bemerkungen = models.TextField(blank=True)
    aktenzeichen = models.CharField("Aktenzeichen", max_length=30)
    pkz = models.CharField("PKZ", max_length=13, blank=True)
    stufe = models.ForeignKey(Stufe, related_name='schueler')
    gruppe = models.ForeignKey(Gruppe, related_name='schueler')
    sozialamt = models.ForeignKey(Sozialamt, related_name='schueler')

    class Meta:
        ordering = ['nachname', 'vorname']
        verbose_name = "Schüler"
        verbose_name_plural = "Schüler"

    def __str__(self):
        return self.voller_name

    @property
    def voller_name(self):
        return "{s.vorname} {s.nachname}".format(s=self)

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
