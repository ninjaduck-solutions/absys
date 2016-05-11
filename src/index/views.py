from django.shortcuts import render
from django.utils import timezone
from .models import Schueler

def schueler_list(request):
    schueler = Schueler.objects.order_by('nname')
    return render(request, 'index/schueler_list.html', {'schueler': schueler})

def index(request):
    return render(request, 'index/index.html')
