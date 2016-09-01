from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from crispy_forms.bootstrap import FormActions
from django import forms

from absys.apps.schueler import models


class RechnungSozialamtForm(forms.Form):

    startdatum = forms.DateField(label="Startdatum")
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
                    Field('startdatum'),
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
