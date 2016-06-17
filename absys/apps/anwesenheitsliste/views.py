from django.views import generic

from . import models


class AnwesenheitslisteView(generic.ListView):
    model = models.Schueler
