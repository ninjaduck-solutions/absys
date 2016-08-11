from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AnmeldungConfig(AppConfig):
    """Configuration for anmeldung app."""

    name = 'absys.apps.anmeldung'
    verbose_name = _("Anmeldung")
