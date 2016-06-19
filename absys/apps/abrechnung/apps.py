from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AbrechnungConfig(AppConfig):
    """Configuration for abrechnung app."""

    name = 'absys.apps.abrechnung'
    verbose_name = _("Abrechnung")
