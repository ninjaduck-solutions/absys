from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DeleteView, FormView
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import MultipleObjectMixin
from extra_views import InlineFormSet, UpdateWithInlinesView

from wkhtmltopdf.views import PDFTemplateView

from . import forms, models


class RechnungSozialamtFormView(LoginRequiredMixin, MultipleObjectMixin, FormView):

    form_class = forms.RechnungSozialamtForm
    success_url = reverse_lazy('abrechnung_rechnungsozialamt_form')
    template_name = 'abrechnung/rechnung_sozialamt_form.html'
    model = models.RechnungSozialamt

    def form_valid(self, form):
        for sozialamt in form.cleaned_data['sozialaemter']:
            try:
                rechnung = models.RechnungSozialamt.objects.rechnungslauf(
                    sozialamt,
                    form.cleaned_data['enddatum']
                )
            except ValidationError as e:
                messages.add_message(self.request, messages.ERROR, [err for err in e.error_dict.values()])
            else:
                messages.add_message(
                    self.request,
                    messages.INFO,
                    "Rechnung Nr. {r.nummer} erstellt".format(r=rechnung)
                )
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().post(request, *args, **kwargs)


class AbrechnungPDFView(BaseDetailView, PDFTemplateView):

    #TODO: prefetch_related() nutzen
    model = models.RechnungSozialamt
    template_name = 'abrechnung/pdf.html'
    cmd_options = {
        'orientation': 'Landscape',
    }

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


class RechnungSozialamtUpdateView(UpdateWithInlinesView):

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


class RechnungSozialamtDeleteView(DeleteView):

    model = models.RechnungSozialamt
    success_url = reverse_lazy('abrechnung_rechnungsozialamt_form')
