from django.urls import path

from . import views

urlpatterns = [
    path(
        r'^(?P<datum>\d{4}-\d{2}-\d{2})/$',
        views.AnwesenheitslisteFormSetView.as_view(),
        name='anwesenheitsliste_anwesenheit_anwesenheitsliste'
    ),
    path(
        r'^$',
        views.AnwesenheitslisteHeuteRedirectView.as_view(),
        name='anwesenheitsliste_anwesenheit_heute'
    )
]
