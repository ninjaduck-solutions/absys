from __future__ import unicode_literals

from django.db import models

from django.utils import timezone


class Schueler(models.Model):
    nname = models.CharField(max_length=200)
    vname = models.CharField(max_length=200)
    geburtsdatum = models.DateField()
    created_date = models.DateTimeField(
            default=timezone.now)
    
    
    
    def __unicode__(self):
        return (self.nname)
    
    #def __unicode__(self):
    #    reutrn self.vname
