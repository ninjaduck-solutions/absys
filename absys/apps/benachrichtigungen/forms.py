from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Field, Layout, Submit


class BenachrichtigungFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Div(
                HTML('<div class="row">{{ form.instance.erstellt}} </div>'),
                HTML('<div class="row">{{ form.instance.text}} </div>'),
                Div(
                    Field('erledigt'),
                ),
            css_class="well"),
        )
