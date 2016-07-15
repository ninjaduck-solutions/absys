from datetime import timedelta

from dateutil.parser import parse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.views.generic import RedirectView
import extra_views

from absys.apps.einrichtungen.models import Einrichtung
from absys.apps.schueler.models import Gruppe, Schueler

from . import forms
from . import models


class AnwesenheitslisteFormSetView(extra_views.FormSetView):

    form_class = forms.AnwesenheitForm
    extra = 0
    template_name = 'anwesenheitsliste/schueler_list.html'

    def get_initial(self):
        data = []
        for schueler in Schueler.objects.filter(gruppe__id=self.gruppe_id):
            try:
                abwesend = schueler.anwesenheit.get(datum=self.datum).abwesend
            except schueler.anwesenheit.model.DoesNotExist:
                abwesend = False
            einrichtung = schueler.get_einrichtung(self.datum)
            if einrichtung is None:
                continue
            data.append({
                'schueler_id': schueler.id,
                'einrichtung_id': einrichtung.id,
                'datum': self.datum,
                'schueler': schueler.voller_name,
                'einrichtung_kuerzel': einrichtung.kuerzel,
                'abwesend': abwesend
            })
        return data

    def formset_valid(self, formset):
        for form in formset:
            models.Anwesenheit.objects.update_or_create(
                schueler=Schueler.objects.get(
                    id=form.cleaned_data['schueler_id']
                ),
                einrichtung=Einrichtung.objects.get(
                    id=form.cleaned_data['einrichtung_id']
                ),
                datum=form.cleaned_data['datum'],
                defaults={'abwesend': form.cleaned_data['abwesend']},
            )
        return super().formset_valid(formset)

    def get_success_url(self):
        return reverse('anwesenheitsliste_anwesenheit_anwesenheitsliste',
            kwargs={'datum': self.datum + timedelta(1)}
        ) + '?' + self.query_string

    @property
    def helper(self):
        return forms.AnwesenheitFormHelper()

    @property
    def datum(self):
        return timezone.make_aware(parse(self.kwargs['datum'])).date()

    @property
    def gestern(self):
        return self.datum + timedelta(-1)

    @property
    def morgen(self):
        return self.datum + timedelta(1)

    @cached_property
    def gruppe_id(self):
        return int(self.request.GET.get('gruppe_id', 0))

    @cached_property
    def gruppen(self):
        return Gruppe.objects.values('id', 'name')

    @cached_property
    def query_string(self):
        if self.gruppe_id:
            query_string = 'gruppe_id={0}'.format(self.gruppe_id)
        else:
            query_string = ''
        return query_string


class AnwesenheitslisteHeuteRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        datum = timezone.now().date()
        return reverse('anwesenheitsliste_anwesenheit_anwesenheitsliste', kwargs={'datum': datum})
