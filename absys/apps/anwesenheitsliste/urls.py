from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<datum>\d{4}-\d{2}-\d{2})/$',
        views.AnwesenheitslisteFormSetView.as_view(),
        name='anwesenheitsliste_anwesenheit_anwesenheitsliste'
    ),
    url(
        r'^$',
        views.AnwesenheitslisteHeuteRedirectView.as_view(),
        name='anwesenheitsliste_anwesenheit_heute'
    )
]
