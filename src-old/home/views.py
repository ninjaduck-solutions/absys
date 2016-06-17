from django.shortcuts import render

# Create your views here.

#Base = Rahmen-Theme, von dem alle anderen Themes abgeleitet werden sollen
from django.http import HttpResponse

def home(request):
    return render(request, 'home/home.html', {})