from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms


class AnwesenheitForm(forms.Form):

    schueler_id = forms.IntegerField(widget=forms.HiddenInput())
    datum = forms.DateField(widget=forms.HiddenInput())
    schueler = forms.CharField(label="", required=False)
    abwesend = forms.BooleanField(required=False)


class AnwesenheitFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_input(Submit('submit', 'Speichern', css_class="btn btn-success"))
        self.layout = Layout(
            Div(
                Div(
                    Field('schueler', disabled=''),
                    css_class='col-md-8 dark'
                ),
                Div(
                    Field('abwesend'),
                    css_class='col-md-3'
                ),
                css_class="row"
            ),
        )
