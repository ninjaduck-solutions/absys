from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import datetime
from django.utils.formats import localize
from django.utils.translation import ugettext



class Gruppe(models.Model):
    gruppenname = models.CharField(max_length=400, default="")
    bemerkungen = models.CharField(max_length=200)
    
    #erstellungsdatum = models.DateTimeField(auto_now_add = True, default="", editable=False)
    erstellungsdatum = models.DateTimeField(default=datetime.now, editable=False)
    
    class Meta:
      verbose_name_plural="Gruppen"
      verbose_name="Gruppe"
      managed=True
    
    def __unicode__(self):
       return self.gruppenname




class Stufe(models.Model):
    stufenname = models.CharField(max_length=400, default="")
    bemerkungen = models.CharField(max_length=200)
    
    #erstellungsdatum = models.DateTimeField(auto_now_add = True, default="", editable=False)
    erstellungsdatum = models.DateTimeField(default=datetime.now, editable=False)
        
    class Meta:
      verbose_name_plural="Stufen"
      verbose_name="Stufe"
      managed=True
      
    def __unicode__(self):
        return self.stufenname




class Einrichtung(models.Model):
    einrichtungsname = models.CharField(max_length=200, default="")
    einrichtungspflegesatz_schultag = models.DecimalField(max_digits=4, decimal_places=2)
    einrichtungspflegesatz_schultag_startdatum = models.DateField()
    einrichtungspflegesatz_schultag_enddatum = models.DateField()
    einrichtungspflegesatz_ferientag = models.DecimalField(max_digits=4, decimal_places=2)
    einrichtungspflegesatz_ferientag_startdatum = models.DateField()
    einrichtungspflegesatz_ferientag_enddatum = models.DateField()
    
    #erstellungsdatum = models.DateTimeField(auto_now_add = True, default="", editable=False)
    erstellungsdatum = models.DateTimeField(default=datetime.now, editable=False)
        
    class Meta:
      verbose_name_plural="Einrichtungen"
      verbose_name="Einrichtung"
      managed=True
    
    def __unicode__(self):
        return self.einrichtungsname




class Sozialamt(models.Model):
    sozialamtname = models.CharField(max_length=200, default="")
    sozialamt_anschrift = models.CharField(max_length=400)
    sozialamt_konto_iban = models.CharField(max_length=22)
    sozialamt_konto_institut = models.CharField(max_length=400)
    
    #erstellungsdatum = models.DateTimeField(auto_now_add = True, default="", editable=False)
    erstellungsdatum = models.DateTimeField(default=datetime.now, editable=False) 
    
    class Meta:
      verbose_name_plural="Sozialaemter"
      verbose_name="Sozialamt"
      managed=True
    
    def __unicode__(self):
        return self.sozialamtname
    
    
 
    
class Schliesstag(models.Model):
    datum = models.DateField()
    art = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=50, blank=True)
    
    #erstellungsdatum = models.DateTimeField(auto_now_add = True, default="", editable=False)
    erstellungsdatum = models.DateTimeField(default=datetime.now, editable=False)
    
    class Meta:
      verbose_name_plural="Schliesstage"
      verbose_name="Schliesstag"
      managed=True
    
    def __unicode__(self):
        return ugettext("%(datum)s") % {
            'datum': localize(self.datum),
        }
    
    
    
    
class Ferien(models.Model):
    ferienname = models.CharField(max_length=30, blank=True)
    startdatum = models.DateField()
    enddatum = models.DateField()
    
    #erstellungsdatum = models.DateTimeField(auto_now_add = True, default="", editable=False)
    erstellungsdatum = models.DateTimeField(default=datetime.now, editable=False)
        
    class Meta:
      verbose_name_plural="Ferien"
      verbose_name="Ferien"
      managed=True
    
    def __unicode__(self):
        return (self.ferienname) + ' ' + ugettext("vom %(startdatum)s bis %(enddatum)s") % {
            'startdatum': localize(self.startdatum),
            'enddatum': localize(self.enddatum),
            }



class Schueler(models.Model):
    
    nachname = models.CharField(max_length=200)
    vorname = models.CharField(max_length=200)
    geburtsdatum = models.DateField()
    bemerkungen = models.TextField(max_length=10000)
    pers_pflegesatz = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    buchungsnummer = models.CharField(max_length=30, blank=True, null=True, default="")
    
    stufe = models.ForeignKey(Stufe, on_delete=models.CASCADE, default="")
    
    #erstellungsdatum = models.DateTimeField(auto_now_add = True, default="", editable=False)
    erstellungsdatum = models.DateTimeField(default=datetime.now, editable=False)
        
    class Meta:
      verbose_name_plural="Schueler"
      verbose_name="Schueler"
      managed=True
    
    def __unicode__(self):
        return (self.nachname) + ', ' + (self.vorname)




#TODO: class PflegesatzDesSchuelers mittels model manager und class realisieren



    
class SchuelerInEinrichtung(models.Model):

    schueler = models.ForeignKey(Schueler, on_delete=models.CASCADE, default="", related_name='+')
    einrichtung = models.ForeignKey(Einrichtung, on_delete=models.CASCADE, default="", related_name='+')

    erstellungsdatum = models.DateTimeField(default=datetime.now, editable=False)
    
    class Meta:
        verbose_name="Schueler in der Einrichtung"
        verbose_name_plural="Schueler in der Einrichtung"
        managed=True
        
    def __unicode__(self):
        return ugettext("%(schueler)s in %(einrichtung)s") % {
            'schueler': localize(self.schueler),
            'einrichtung': localize(self.einrichtung)
            }
    