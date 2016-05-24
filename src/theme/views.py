from django.shortcuts import render

# Create your views here.

#Standard-Layout zum Holen von Templatestueckchen
def theme(request):
    return render(request, 'theme/theme.html', {})