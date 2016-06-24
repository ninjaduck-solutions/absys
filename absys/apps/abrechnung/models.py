from django.db import models
#from django.utils.timezone import now
from django.utils.functional import cached_property
#from datetime import datetime

# # TODO: CONSTRAINTS mit clean() (siehe ModelValidation in DjangoDocs)
# # TODO: Schueler kann inaktiv gesetzt werden -> Datensätze bleiben erhalten, wird aber nicht mehr berücksichtigt


class Gruppe(models.Model):

    name = models.CharField(max_length=5, default="")
    bemerkungen = models.CharField(max_length=200)
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
      verbose_name_plural="Gruppen"
      verbose_name="Gruppe"

    def __str__(self):
       return self.name


class Stufe(models.Model):

    name = models.CharField(max_length=5, default="")
    bemerkungen = models.CharField(max_length=200)
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
      verbose_name_plural="Stufen"
      verbose_name="Stufe"

    def __str__(self):
        return self.name


class Einrichtung(models.Model):

    name = models.CharField(max_length=15)
    kuerzel = models.CharField(max_length=1)
    
    class Meta:
      verbose_name_plural="Einrichtungen"
      verbose_name="Einrichtung"

    def __str__(self):
        return self.kuerzel


class Ferien(models.Model):

    name = models.CharField(max_length=10)
    startdatum = models.DateField()
    enddatum = models.DateField()
    einrichtungen = models.ManyToManyField(Einrichtung, verbose_name='Einrichtungen', related_name='ferien')
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
      verbose_name_plural="Ferien"
      verbose_name="Ferien"

    def __str__(self):
        return self.name


class Sozialamt(models.Model):

    name = models.CharField(max_length=10, default="")
    anschrift = models.CharField(max_length=20)
    konto_iban = models.CharField(max_length=22)
    konto_institut = models.CharField(max_length=10)
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
      verbose_name_plural="Sozialaemter"
      verbose_name="Sozialamt"

    def __str__(self):
        return self.name


class Schliesstag(models.Model):

    datum = models.DateField()
    art = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=5, blank=True)
    einrichtungen = models.ManyToManyField(Einrichtung, verbose_name='Einrichtungen', related_name='schliesstage')

    class Meta:
      verbose_name_plural="Schliesstage"
      verbose_name="Schliesstag"

    def __str__(self):
        return '{s.name}: {s.datum}) '.format(s=self)


class Schueler(models.Model):

    nachname = models.CharField(max_length=10)
    vorname = models.CharField(max_length=10)
    geburtsdatum = models.DateField()
    bemerkungen = models.TextField(max_length=100)
    buchungsnummer = models.CharField(max_length=13, blank=True)
    stufe = models.ForeignKey(Stufe)
    gruppe = models.ForeignKey(Gruppe)
    sozialamt = models.ForeignKey(Sozialamt)
    einrichtungen = models.ManyToManyField(Einrichtung, through='SchuelerInEinrichtung')
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
      verbose_name_plural="Schueler"
      verbose_name="Schueler"

    def __str__(self):
        return '{s.nachname}, {s.vorname}'.format(s=self)


class FehltageSchuelerErlaubt(models.Model):

    schueler = models.ForeignKey(Schueler)
    wert = models.PositiveIntegerField(default=45)
    startdatum = models.DateField()
    enddatum = models.DateField()
    jahr = models.CharField(max_length=4)

    class Meta:
        verbose_name_plural = "Erlaubte Fehltage von Schuelern"
        verbose_name = "Erlaubte Fehltage eines Schuelers"

    def __str__(self):
        return '{s.schueler}  | {s.startdatum} - {s.enddatum} | {s.wert}'.format(s=self)


class SchuelerInEinrichtung(models.Model):

    schueler = models.ForeignKey(Schueler)
    einrichtung = models.ForeignKey(Einrichtung)
    eintritt = models.DateField()
    austritt = models.DateField()
    sozialamtbescheid_von = models.DateField()
    sozialamtbescheid_bis = models.DateField()
    pers_pflegesatz = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    pers_pflegesatz_startdatum = models.DateField(blank=True, null=True)
    pers_pflegesatz_enddatum = models.DateField(blank=True, null=True)
    pers_pflegesatz_ferien = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    pers_pflegesatz_ferien_startdatum = models.DateField(blank=True, null=True)
    pers_pflegesatz_ferien_enddatum = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('schueler', 'einrichtung', 'eintritt', 'austritt')
        verbose_name_plural = "Schueler in den Einrichtungen"
        verbose_name = "Schueler in der Einrichtung"
        ordering = ("schueler__nachname", "schueler__vorname", "-austritt")

    def __str__(self):
        return '{s.schueler} in {s.einrichtung} ({s.eintritt} - {s.austritt}) '.format(s=self)

#     def pflegesatz(self, datum=None):
#         if self.pers_pflegesatz:
#             return self.pers_pflegesatz
#         if not datum:
#             datum = now().date
#         return SchuelerInEinrichtung.objects.filter(schueler=self, austritt__lte=datum).first().einrichtung.pflegesatz

class EinrichtungHatPflegesatz(models.Model):

    name = models.ForeignKey(Einrichtung)
    pflegesatz = models.DecimalField(max_digits=4, decimal_places=2)
    pflegesatz_startdatum = models.DateField()
    pflegesatz_enddatum = models.DateField()
    pflegesatz_ferien = models.DecimalField(max_digits=4, decimal_places=2)
    pflegesatz_ferien_startdatum = models.DateField()
    pflegesatz_ferien_enddatum = models.DateField()
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
      verbose_name_plural="Pflegesätze in den Einrichtungen"
      verbose_name="Pflegesatz der Einrichtung"

    def __str__(self):
        return '{s.name} | {s.pflegesatz} | {s.pflegesatz_ferien}'.format(s=self)

class Anwesenheit(models.Model):

    schueler = models.ForeignKey(Schueler)
    datum = models.DateField()
    anwesenheit = models.CharField(max_length=1)
    abgerechnet = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Anwesenheiten der Schueler"
        verbose_name = "Anwesenheit eines Schueler in einer Einrichtung"
        unique_together = ('schueler', 'datum', 'abgerechnet')

    def __str__(self):
        return  '{s.schueler} am {s.datum} | {s.anwesenheit}'.format(s=self)

    #def anzahlAnwesenheit

    #def anzahlFehltage
