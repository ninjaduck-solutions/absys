from django.db import models
from django.utils.timezone import datetime


# Create your models here.

class Gruppe(models.Model):
    gruppenname = models.CharField(max_length=400, default='1')
    bemerkungen = models.CharField(max_length=200)

    def __unicode__(self):
       return self.gruppenname



class Stufe(models.Model):
    stufenname = models.CharField(max_length=400, default='1')
    bemerkungen = models.CharField(max_length=200)

    def __unicode__(self):
        return self.stufenname



class Schueler(models.Model):
    
    nachname = models.CharField(max_length=200)
    vorname = models.CharField(max_length=200)
    geburtsdatum = models.DateField()
    bemerkungen = models.TextField(max_length=10000)
    
    gruppe = models.ForeignKey(Gruppe, on_delete=models.CASCADE, default='1')
    stufe = models.ForeignKey(Stufe, on_delete=models.CASCADE, default='1')
    
    erstellungsdatum = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return self.nachname
    

    