from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.RechnungSozialamtFormView.as_view(),
        name='abrechnung_rechnungsozialamt_form'
    ),
]
