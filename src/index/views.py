from django.shortcuts import render, render_to_response, RequestContext
from django.utils import timezone
from .models import Schueler

def schueler_list(request):
    schueler = Schueler.objects.order_by('nname')
    return render_to_response('index/schueler_list.html', {'schueler': schueler})

def index(request):
    return render_to_response('index/index.html')

def base(request):
    schueler = Schueler.objects.order_by('nname')
    return render_to_response('index/base.html', {'schueler': schueler})
