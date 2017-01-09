import django_filters

from . import models


class BenachrichtigungFilter(django_filters.FilterSet):
    #erledigt = django_filters.BooleanFilter(initial=2)

    class Meta:
        model = models.Benachrichtigung
        fields = ('erledigt',)
