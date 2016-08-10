from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SchuelerConfig(AppConfig):
    """Configuration for schueler app."""

    name = 'absys.apps.schueler'
    verbose_name = _("Schüler")
