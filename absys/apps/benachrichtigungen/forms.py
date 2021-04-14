from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Field, Layout, Submit


class BenachrichtigungFormSetHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = True
        self.form_method = 'post'
        self.render_unmentioned_fields = True
        self.layout = Layout(
            Div(
                HTML('<div class="row">{{ formset_form.instance.erstellt }}</div>'),
                HTML('<div class="row">{{ formset_form.instance.text }}</div>'),
                Div(
                    Field('erledigt'),
                ),
                css_class="well"),
        )
        self.add_input(Submit('submit', 'Senden'))
