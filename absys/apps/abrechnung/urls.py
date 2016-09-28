from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.RechnungSozialamtFormView.as_view(),
        name='abrechnung_rechnungsozialamt_form'
    ),
    url(r'^(?P<pk>[\d]+)/pdf',
        views.AbrechnungPDFView.as_view(),
        name='abrechnung_rechnungsozialamt_pdf'
    ),
    url(r'^(?P<pk>[\d]+)/saxmbs/', views.SaxmbsView.as_view(),
        name='abrechnung_saxmbs_dat'
    ),
]
