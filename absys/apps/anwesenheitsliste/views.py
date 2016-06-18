from datetime import timedelta

from dateutil.parser import parse
from django.core.urlresolvers import reverse
from django.utils import timezone
import extra_views

from . import forms
from . import models


class AnwesenheitslisteFormSetView(extra_views.FormSetView):
    form_class = forms.AnwesenheitForm
    extra = 0
    template_name = 'anwesenheitsliste/schueler_list.html'

    def get_initial(self):
        data = []
        for schueler in models.Schueler.objects.all():
            try:
                abwesend = schueler.anwesenheit.get(datum=self.datum).abwesend
            except schueler.anwesenheit.model.DoesNotExist:
                abwesend = False
            data.append({
                'schueler_id': schueler.id,
                'einrichtungs_art_id': schueler.einrichtungs_art.id,
                'datum': self.datum,
                'schueler': schueler.voller_name,
                'einrichtungs_art_kuerzel': schueler.einrichtungs_art.kuerzel,
                'abwesend': abwesend
            })
        return data

    def formset_valid(self, formset):
        for form in formset:
            models.Anwesenheit.objects.update_or_create(
                schueler=models.Schueler.objects.get(
                    id=form.cleaned_data['schueler_id']
                ),
                einrichtungs_art=models.EinrichtungsArt.objects.get(
                    id=form.cleaned_data['einrichtungs_art_id']
                ),
                datum=form.cleaned_data['datum'],
                defaults={'abwesend': form.cleaned_data['abwesend']},
            )
        return super().formset_valid(formset)

    def get_success_url(self):
        return reverse('anwesenheitsliste_anwesenheit_anwesenheitsliste',
            kwargs={'datum': self.datum + timedelta(1)}
        )

    @property
    def helper(self):
        return forms.AnwesenheitFormHelper()

    @property
    def datum(self):
        return timezone.make_aware(parse(self.kwargs['datum'])).date()
