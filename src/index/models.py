from __future__ import unicode_literals

from django.db import models

from django.utils import timezone


class Schueler(models.Model):
    nname = models.CharField(max_length=200)
    vname = models.CharField(max_length=200)
    geburtsdatum = models.DateField()
    created_date = models.DateTimeField(
            default=timezone.now)
    
    def __str__(self):
        return self.nname
