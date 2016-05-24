"""absys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .views import *
from stammdaten import views

urlpatterns = [
        #url(r'^(?P<pk>\d+)', 'schueler.views.SchuelerDetail', name='schueler_detail'),
        #url(r'^gruppe/(?P<pk>\d+)', 'schueler.views.GruppeDetail', name='gruppe_detail'),
        #url(r'^$/', SchuelerList.as_view()),
        url(r'^gruppen/', GruppeList.as_view()),
        url(r'^stufen/', StufeList.as_view()),
        url(r'^einrichtungen/', EinrichtungList.as_view()),
        url(r'^sozialaemter/', SozialamtList.as_view()),
        url(r'^schliesstage/', SchliesstagList.as_view()),
        url(r'^ferien/', FerienList.as_view()),
        url(r'^schueler/', SchuelerList.as_view()),
        url(r'^schuelerineinrichtung/', SchuelerInEinrichtungList.as_view()),
        
        url(r'^', views.stammdaten, name='stammdaten'),
]
