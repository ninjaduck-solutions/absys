from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DeleteView, FormView
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import MultipleObjectMixin
from dateutil import parser
from extra_views import FormSetView, InlineFormSet, UpdateWithInlinesView

from wkhtmltopdf.views import PDFTemplateView

from absys.apps.schueler.models import Sozialamt
from . import forms, models, responses


class RechnungSozialamtFormView(LoginRequiredMixin, MultipleObjectMixin, FormView):
    """
    Daten zur Erstellung von :model:`abrechnung.RechnungSozialamt`-Instanzen sammeln.

    Nach der Validierung der Daten muss geprüft werden, ob mit diesen Daten
    :model:`abrechnung.RechnungSozialamt`-Instanzen erstellt werden können.
    Falls nicht, wird mit das Formular erneut mit einer einer Fehlermeldung
    angezeigt.

    Danach muss in einem weiteren View ermittelt werden, ob Bekleidungsgeld
    gezahlt wird und dieses ggf. pro Schüler in Einrichtung manuell erfasst
    werden. Dann kann in dem View zur Erfassung des Bekleidungsgelds der
    Rechnungslauf gestartet werden.
    """

    form_class = forms.RechnungSozialamtForm
    success_url = reverse_lazy('abrechnung_erfassung_bekleidungsgeld_form')
    template_name = 'abrechnung/rechnung_sozialamt_form.html'
    model = models.RechnungSozialamt

    def form_valid(self, form):
        for sozialamt in form.cleaned_data['sozialaemter']:
            try:
                models.RechnungSozialamt.objects.vorbereiten(
                    sozialamt,
                    form.cleaned_data['enddatum']
                )
            except ValidationError as e:
                for field, error in e.error_dict.items():
                    form.add_error(field, error)
                return self.form_invalid(form)
        self.query_string = 'sozialaemter={0}&enddatum={1}'.format(
            ','.join(map(str, form.cleaned_data['sozialaemter'].values_list('pk', flat=True))),
            form.cleaned_data['enddatum']
        )
        return super().form_valid(form)

    def get_success_url(self):
        return '{0}?{1}'.format(super().get_success_url(), self.query_string)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().post(request, *args, **kwargs)


class ErfassungBekleidungsgeldFormView(LoginRequiredMixin, FormSetView):
    """
    Erfassung des Bekleidungsgelds pro Schüler in Einrichtung.

    Das Bekleidungsgeld wird pro Schüler in Einrichtung gezahlt und muss
    manuell erfasst werden. Dies ist allerdings nur für die Einrichtungen
    nötig, die auch ein Bekleidungsgeld auszahlen.

    Nach der Erfassung wird der Rechnungslauf zur Erstellung der
    :model:`abrechnung.RechnungSozialamt`-Instanzen gestartet.
    """

    form_class = forms.ErfassungBekleidungsgeldForm
    extra = 0
    success_url = reverse_lazy('abrechnung_rechnungsozialamt_form')
    template_name = 'abrechnung/erfassung_bekleidungsgeld.html'

    def get_initial(self):
        """
        Schüler in Einrichtungen laden, für die Bekleidungsgeld erfasst werden muss.
        """
        self.initial = []
        for sozialamt in self.sozialaemter:
            qs = sozialamt.anmeldungen.zeitraum(self.startdatum, self.enddatum)
            for schueler_in_einrichtung in qs:
                if not schueler_in_einrichtung.einrichtung.konfiguration.bekleidungsgeld:
                    continue
                self.initial.append({
                    'schueler_in_einrichtung_id': schueler_in_einrichtung.pk,
                    'schueler': schueler_in_einrichtung.schueler,
                    'einrichtung': schueler_in_einrichtung.einrichtung,
                    'bekleidungsgeld': 0.0
                })
        return super().get_initial()

    def formset_valid(self, formset):
        """
        Rechnungslauf starten.

        Falls erfasst, wird das Bekleidungsgeld abgerechnet.
        """
        bekleidungsgeld = {}
        for form in formset:
            data = form.cleaned_data
            bekleidungsgeld[data['schueler_in_einrichtung_id']] = data['bekleidungsgeld']
        for sozialamt in self.sozialaemter:
            rechnung_sozialamt = models.RechnungSozialamt.objects.rechnungslauf(
                sozialamt, self.enddatum, bekleidungsgeld
            )
            messages.add_message(
                self.request,
                messages.INFO,
                "Rechnung Nr. {r.nummer} erstellt".format(r=rechnung_sozialamt)
            )
        return super().formset_valid(formset)

    @cached_property
    def sozialaemter(self):
        """
        Gibt alle Sozialämter aus dem Query String zurück.
        """
        return Sozialamt.objects.filter(pk__in=self.request.GET.get('sozialaemter').split(','))

    @cached_property
    def startdatum(self):
        """
        Gibt das Startdatum aus dem Query String zurück.
        """
        return models.RechnungSozialamt.objects.get_startdatum(self.sozialaemter[0], self.enddatum)

    @property
    def enddatum(self):
        """
        Gibt das Enddatum aus dem Query String zurück.
        """
        return parser.parse(self.request.GET.get('enddatum')).date()

    @property
    def helper(self):
        """
        Gibt den FormHelper zum Erfassen des Bekleidungsgelds zurück.
        """
        return forms.ErfassungBekleidungsgeldFormHelper(bool(len(self.initial)))


class AbrechnungPDFView(LoginRequiredMixin, BaseDetailView, PDFTemplateView):

    # TODO: prefetch_related() nutzen
    model = models.RechnungSozialamt
    template_name = 'abrechnung/pdf.html'
    cmd_options = {
        'orientation': 'Landscape',
    }

    @property
    def adresse_schule(self):
        return settings.ABSYS_ADRESSE_SCHULE

    @property
    def filename(self):
        return '{}-{}_{}-{}.pdf'.format(
            self.object.startdatum,
            self.object.enddatum,
            self.object.sozialamt,
            self.object.nummer,
        )


class RechnungEinrichtungInline(InlineFormSet):

    model = models.RechnungEinrichtung
    fields = ('id', 'buchungskennzeichen', 'datum_faellig')
    can_delete = False
    extra = 0


class RechnungSozialamtUpdateView(LoginRequiredMixin, UpdateWithInlinesView):

    model = models.RechnungSozialamt
    fields = ('name_sozialamt', 'anschrift_sozialamt')
    inlines = [RechnungEinrichtungInline]
    success_url = reverse_lazy('abrechnung_rechnungsozialamt_form')

    @property
    def helper_sozialamt(self):
        return forms.RechnungSozialamtUpdateFormHelper()

    @property
    def helper_einrichtung(self):
        return forms.RechnungEinrichtungUpdateFormHelper()


class RechnungSozialamtDeleteView(LoginRequiredMixin, DeleteView):

    model = models.RechnungSozialamt
    success_url = reverse_lazy('abrechnung_rechnungsozialamt_form')

    def kandidaten(self):
        return models.RechnungSozialamt.objects.seit(self.object.startdatum)


class SaxmbsView(LoginRequiredMixin, BaseDetailView):

    model = models.RechnungSozialamt

    def render_to_response(self, context):
        return responses.SaxMBSResponse(self.object)
