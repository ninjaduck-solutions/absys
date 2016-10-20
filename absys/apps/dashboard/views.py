from django.http import HttpResponse

from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/dashboard.html'