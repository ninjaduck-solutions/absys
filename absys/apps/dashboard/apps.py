from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DashboardConfig(AppConfig):
    """Configuration for dashboard app."""

    name = 'absys.apps.dashboard'
    verbose_name = _("Dashboard")
