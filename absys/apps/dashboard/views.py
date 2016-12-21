from django.http import HttpResponse
from django.shortcuts import redirect

from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Leite direkt zur Anwesenheitsliste weiter wenn dies die *einzigen* Rechte sind.

        Note:
            Es geht nicht darum das mindestens ``erwartete_rechte`` vorliegen müssen sondern den
            speziellen Fall das dies auch die *einzigen* Rechte sind.
        """
        erwartete_rechte = ('anwesenheitsliste.add_anwesenheit', 'anwesenheitsliste.change_anwesenheit')
        if request.user.get_all_permissions() == set(erwartete_rechte):
            return redirect('anwesenheitsliste_anwesenheit_heute')
        return super().dispatch(request, *args, **kwargs)
