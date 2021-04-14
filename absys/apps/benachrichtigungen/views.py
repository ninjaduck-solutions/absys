from extra_views import ModelFormSetView
from braces.views import PermissionRequiredMixin

from . import forms
from . import models
from . import filters


class BenachrichtigungListView(PermissionRequiredMixin, ModelFormSetView):
    model = models.Benachrichtigung
    fields = ('id', 'erledigt')
    template_name = 'benachrichtigungen/benachrichtigung_list.html'
    factory_kwargs = {'extra': 0}

    permission_required = 'benachrichtigungen.change_benachrichtigung'

    @property
    def formset_helper(self):
        return forms.BenachrichtigungFormSetHelper()

    @property
    def filter(self):
        qs = self.model.objects.all()
        data = self.request.GET.copy()
        # Set default filter value. Previously this was done in the filter class,
        # a behavior deprecated by now.
        if not data.get('erledigt'):
            data['erledigt'] = 'false'
        return filters.BenachrichtigungFilter(data, queryset=qs)

    def get_queryset(self, *args, **kwargs):
        return self.filter.qs
