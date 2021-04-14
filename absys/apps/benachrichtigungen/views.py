from extra_views import ModelFormSetView
from braces.views import PermissionRequiredMixin

from . import forms
from . import models
from . import filters


class BenachrichtigungListView(PermissionRequiredMixin, ModelFormSetView):
    model = models.Benachrichtigung
    fields = ('id', 'erledigt',)
    template_name = 'benachrichtigungen/benachrichtigung_list.html'
    factory_kwargs = {'extra': 0}

    permission_required = 'benachrichtigungen.change_benachrichtigung'

    @property
    def helper(self):
        return forms.BenachrichtigungFormHelper()

    @property
    def filter(self):
        qs = self.model.objects.all()
        data = self.request.GET.copy()
        print(data)
        if len(data) == 0:
            data['erledigt'] = '3'
        return filters.BenachrichtigungFilter(data, queryset=qs)

    def get_queryset(self, *args, **kwargs):
        return self.filter.qs
