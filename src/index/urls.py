from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^schueler_list$', views.schueler_list, name='schueler_list'),
    url(r'', views.index),
    
]