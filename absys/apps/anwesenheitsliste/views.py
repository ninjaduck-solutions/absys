from datetime import timedelta, date

from braces.views import LoginRequiredMixin, MultiplePermissionsRequiredMixin
from dateutil.parser import parse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.views.generic import RedirectView
import extra_views

from absys.apps.schueler.models import Gruppe, Schueler

from . import forms
from .models import Anwesenheit


class AnwesenheitslisteFormSetView(LoginRequiredMixin, MultiplePermissionsRequiredMixin,
        extra_views.FormSetView):

    form_class = forms.AnwesenheitForm
    template_name = 'anwesenheitsliste/schueler_list.html'
    factory_kwargs = {'extra': 0}

    permissions = {"all": ('anwesenheitsliste.add_anwesenheit',
                           'anwesenheitsliste.change_anwesenheit')
                   }
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not self.ist_datum_erlaubt(self.datum):
            raise PermissionDenied(
                'Sie haben nicht die Berechtigung, für diesen Tag die Anwesenheiten zu ändern.'
                'Nutzen Sie die "Zurück"-Taste ihre Browsers, um zur Anweseneheitsliste zurückzukehren.'
            )
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        data = []
        for schueler in Schueler.objects.ist_aktiv().filter(gruppe__id=self.gruppe_id):
            try:
                abwesend = schueler.anwesenheit.get(datum=self.datum).abwesend
            except schueler.anwesenheit.model.DoesNotExist:
                abwesend = False
            data.append({
                'schueler_id': schueler.id,
                'datum': self.datum,
                'schueler': schueler.voller_name,
                'abwesend': abwesend
            })
        return data

    def formset_valid(self, formset):
        for form in formset:
            Anwesenheit.objects.update_or_create(
                schueler=Schueler.objects.get(
                    id=form.cleaned_data['schueler_id']
                ),
                datum=form.cleaned_data['datum'],
                defaults={'abwesend': form.cleaned_data['abwesend']},
            )
        return super().formset_valid(formset)

    def get_success_url(self):
        return reverse(
            'anwesenheitsliste_anwesenheit_anwesenheitsliste',
            kwargs={'datum': self.morgen or self.datum}
        ) + '?' + self.query_string

    @property
    def helper(self):
        return forms.AnwesenheitFormHelper()

    @property
    def komplett_erfasst(self):
        schueler = Gruppe.objects.get(id=self.gruppe_id).schueler.count()
        anwesenheiten = Anwesenheit.objects.filter(
            schueler__gruppe__id=self.gruppe_id, datum=self.datum
        ).count()
        return schueler == anwesenheiten

    @property
    def datum(self):
        return timezone.make_aware(parse(self.kwargs['datum'])).date()

    @cached_property
    def heute(self):
        return date.today()

    @cached_property
    def gestern(self):
        gestern = self.datum + timedelta(-1)
        if self.ist_datum_erlaubt(gestern):
            return gestern
        return None

    @cached_property
    def morgen(self):
        morgen = self.datum + timedelta(1)
        if self.ist_datum_erlaubt(morgen):
            return morgen
        return None

    @cached_property
    def aktueller_monat_anfang(self):
        return date.today().replace(day = 1)

    @cached_property
    def vormonat_anfang(self):
        """
        Liefere den den 1ten des Monats vor 'heute'

        Returns:
            date: Datum des ersten Tages des Vormonats relativ zu 'heute'.
                Liefert ``None`` falls dieses Datum 'nicht erlaubt' ist.
        """
        anfang = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1)
        if self.ist_datum_erlaubt(anfang):
            return anfang
        return None

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

    @classmethod
    def ist_aktueller_monat(cls, datum):
        """Überprüft, ob das Datum im aktuellen Monat liegt."""
        return (
            datum.month == timezone.now().date().month and
            datum.year == timezone.now().date().year
        )

    @classmethod
    def ist_vormonat_erlaubt(cls, datum):
        """
        Überprüft, ob das Datum berechtigt den Vormonat zu bearbeiten.

        Note:
            Entgegen des Methodennamens soll hier per Anforderung auch geprüft
            werden das das Datum im Vormonat liegt!
        """
        heute_ok = timezone.now().date().day <= settings.ABSYS_ANWESENHEIT_TAGE_VORMONAT_ERLAUBT
        vormonat_ende = timezone.now().date().replace(day=1) - timedelta(1)
        vormonat_start = vormonat_ende.replace(day=1)
        datum_in_vormonat_ok = vormonat_start <= datum <= vormonat_ende
        return heute_ok and datum_in_vormonat_ok

    @classmethod
    def ist_nicht_in_zukunft(cls, datum):
        return datum <= timezone.now().date()

    @classmethod
    def ist_datum_erlaubt(cls, datum):
        if not settings.ABSYS_ANWESENHEIT_DATUMSPRUEFUNG:
            return True
        return (
            cls.ist_aktueller_monat(datum) and cls.ist_nicht_in_zukunft(datum)
        ) or cls.ist_vormonat_erlaubt(datum)


class AnwesenheitslisteHeuteRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        datum = timezone.now().date()
        return reverse('anwesenheitsliste_anwesenheit_anwesenheitsliste', kwargs={'datum': datum})
