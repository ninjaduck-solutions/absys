from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms


class AnwesenheitForm(forms.Form):

    schueler_id = forms.IntegerField(widget=forms.HiddenInput())
    einrichtungs_art_id = forms.IntegerField(widget=forms.HiddenInput())
    datum = forms.DateField(widget=forms.HiddenInput())
    schueler = forms.CharField(label="", required=False)
    einrichtungs_art_kuerzel = forms.CharField(label="", required=False)
    abwesend = forms.BooleanField(required=False)


class AnwesenheitFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_input(Submit('submit', 'Speichern'))
        self.layout = Layout(
            Div(
                Div(
                    Field('schueler',  disabled=''),
                    css_class='col-md-8'
                ),
                Div(
                    Field('einrichtungs_art_kuerzel',  disabled=''),
                    css_class='col-md-1'
                ),
                Div(
                    Field('abwesend'),
                    css_class='col-md-3'
                ),
                css_class="row"
            ),
        )
