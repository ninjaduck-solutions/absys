from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BenachrichtigungenConfig(AppConfig):
    """Configuration for benachrichtigungen app."""

    name = 'absys.apps.benachrichtigungen'
    verbose_name = _("Benachrichtigungen")
