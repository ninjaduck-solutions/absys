from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, HTML, Layout, Submit
from crispy_forms.bootstrap import FormActions
from django import forms

from absys.apps.schueler import models


class RechnungSozialamtForm(forms.Form):

    enddatum = forms.DateField(
        label="Enddatum",
        help_text=("Das Enddatum muss nach dem Startdatum liegen, "
            "darf aber nicht nach dem heutigen Datum liegen."
            " Außerdem müssen Startdatum und Enddatum im gleichen Jahr liegen.")
    )
    sozialaemter = forms.ModelMultipleChoiceField(
        queryset=models.Sozialamt.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML("<p><strong>Das Startdatum wird für jedes Sozialamt automatisch ermittelt.</strong></p>"),
                    Div(
                        HTML(
                            "Existiert schon eine Rechnung für das Sozialamt, ist das Startdatum der Tag nach dem Enddatum der letzten Rechnung. Ansonsten ist es der 1. Januar des Jahres, das im Enddatum angegeben ist."
                        ),
                        css_class='help-block'
                    ),
                    css_class='col-md-4'
                ),
                Div(
                    Field('enddatum'),
                    css_class='col-md-4'
                ),
                Div(
                    Field('sozialaemter'),
                    css_class='col-md-4'
                ),
                css_class="row"
            ),
            FormActions(
                Submit('submit', "Rechnungen erstellen", css_class="btn btn-success")
            )
        )


class RechnungSozialamtUpdateFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Div(
                Div(
                    Field('name_sozialamt'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('anschrift_sozialamt', rows=5),
                    css_class='col-md-6'
                ),
                css_class="row"
            ),
        )


class RechnungEinrichtungUpdateFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Div(
                Div(
                    Field('buchungskennzeichen'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('datum_faellig'),
                    css_class='col-md-6'
                ),
                css_class="row"
            ),
        )
