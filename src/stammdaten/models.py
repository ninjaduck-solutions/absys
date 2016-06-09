from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now


# TODO: CONSTRAINTS mit clean() (siehe ModelValidation in DjangoDocs)

class Gruppe(models.Model):
    name = models.CharField(max_length=400, default="")
    bemerkungen = models.CharField(max_length=200)
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
      verbose_name_plural="Gruppen"
      verbose_name="Gruppe"  
    
    def __unicode__(self):
       return self.name


class Stufe(models.Model):
    name = models.CharField(max_length=400, default="")
    bemerkungen = models.CharField(max_length=200)
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)
        
    class Meta:
      verbose_name_plural="Stufen"
      verbose_name="Stufe"
      
    def __unicode__(self):
        return self.name


class Einrichtung(models.Model):
    name = models.CharField(max_length=200)
    pflegesatz = models.DecimalField(max_digits=4, decimal_places=2)
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)
        
    class Meta:
      verbose_name_plural="Einrichtungen"
      verbose_name="Einrichtung"  
    
    def __unicode__(self):
        return self.name


class Ferien(models.Model):
    name = models.CharField(max_length=200)
    startdatum = models.DateField()
    enddatum = models.DateField()
    einrichtungen = models.ManyToManyField(Einrichtung, verbose_name='Einrichtungen', related_name='ferien')
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
      verbose_name_plural="Ferien"
      verbose_name="Ferien"  
    
    def __unicode__(self):
        return self.name    

    
class Sozialamt(models.Model):
    name = models.CharField(max_length=200, default="")
    anschrift = models.CharField(max_length=400)
    konto_iban = models.CharField(max_length=22)
    konto_institut = models.CharField(max_length=400)
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
      verbose_name_plural="Sozialaemter"
      verbose_name="Sozialamt"
    
    def __unicode__(self):
        return self.name
    

class Schliesstag(models.Model):
    datum = models.DateField()
    art = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=50, blank=True)
    einrichtungen = models.ManyToManyField(Einrichtung, verbose_name='Einrichtungen', related_name='schliesstage')
    
    class Meta:
      verbose_name_plural="Schliesstage"
      verbose_name="Schliesstag"  
    
    def __unicode__(self):
        return '{s.name}: {s.datum}) '.format(s=self)
        

class Schueler(models.Model):
    
    nachname = models.CharField(max_length=200)
    vorname = models.CharField(max_length=200)
    geburtsdatum = models.DateField()
    bemerkungen = models.TextField(max_length=10000)
    pers_pflegesatz = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    buchungsnummer = models.CharField(max_length=30, blank=True)
    stufe = models.ForeignKey(Stufe)
    gruppe = models.ForeignKey(Gruppe)
    sozialamt = models.ForeignKey(Sozialamt)
    einrichtungen = models.ManyToManyField(Einrichtung, through='SchuelerInEinrichtung')
    erstellungsdatum = models.DateTimeField(auto_now_add=True, editable=False)
        
    class Meta:
      verbose_name_plural="Schueler"
      verbose_name="Schueler"

    def __unicode__(self):
        return '{s.nachname}, {s.vorname}'.format(s=self)


#TODO: class PflegesatzDesSchuelers mittels model manager und class realisieren

    
class SchuelerInEinrichtung(models.Model):

    schueler = models.ForeignKey(Schueler)
    einrichtung = models.ForeignKey(Einrichtung)
    eintritt = models.DateField()
    austritt = models.DateField()
    sozialamtbescheid_von = models.DateField()
    sozialamtbescheid_bis = models.DateField()
    
    class Meta:
        unique_together = ('schueler', 'einrichtung', 'eintritt', 'austritt')
        verbose_name_plural = "Schueler in den Einrichtungen"
        verbose_name = "Schueler in der Einrichtung"
        
    def __unicode__(self):
        return '{s.schueler} in {s.einrichtung} ({s.eintritt} - {s.austritt}) '.format(s=self)
    
    
class Anwesenheit(models.Model):
    
    schueler = models.ForeignKey(Schueler)
    anwesend = models.BooleanField(default=True)
    datum = models.DateField(default=now)
    
    class Meta:
        verbose_name_plural = "Anwesenheiten"
        verbose_name = "Anwesenheit"
        unique_together = ('schueler', 'datum')
        
    def __unicode__(self):
        return '{s.schueler} ({s.datum}) '.format(s=self)
    
    