from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BuchungskennzeichenConfig(AppConfig):
    """Configuration for buchungskennzeichen app."""

    name = 'absys.apps.buchungskennzeichen'
    verbose_name = _("Buchungskennzeichen")
