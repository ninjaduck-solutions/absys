from django.http import HttpResponse
from django.shortcuts import render_to_response
from .models import *
from django.views.generic import ListView

def stammdaten(request):
   return render_to_response('stammdaten/stammdaten.html', {})


class GruppeList(ListView):
    model = Gruppe
    
class StufeList(ListView):
    model = Stufe
    
class EinrichtungList(ListView):
    model = Einrichtung
    
class SozialamtList(ListView):
    model = Sozialamt
    
class SchliesstagList(ListView):
    model = Schliesstag
    
class FerienList(ListView):
    model = Ferien
    
class SchuelerList(ListView):
    model = Schueler
    
class SchuelerInEinrichtungList(ListView):
    model = SchuelerInEinrichtung
