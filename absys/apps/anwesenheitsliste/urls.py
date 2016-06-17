from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.AnwesenheitslisteView.as_view(),
        name='anwesenheitsliste_anwesenheit_anwesenheitsliste'
    ),
]
