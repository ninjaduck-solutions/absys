from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from .models import Schueler, Gruppe, Stufe
from django.views.generic import ListView




#Generische ListView Schuelerliste
class SchuelerList(ListView):
    model = Schueler





 #Generische DetailView Schueler
def SchuelerDetail(request, pk):
    schueler = get_object_or_404(Schueler, pk=pk)
    return render(request, 'schueler/schueler_detail.html', {'schueler': schueler})


#Generische DetailView Gruppe
def GruppeDetail(request, pk):
    gruppe = get_object_or_404(Gruppe, pk=pk)
    return render(request, 'schueler/gruppe_detail.html', {'gruppe': gruppe})