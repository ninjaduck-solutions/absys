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

urlpatterns = [
    #Admin-Panel
    url(r'^backendadmin/', include (admin.site.urls)),
    
    #base.html f?r Entwicklung; sp?ter auskommentieren, alle "richtigen" Views soll davon erben
    url(r'^base/', include ('base.urls')),
    
    #Schueler-App
    url(r'^schueler/', include ('schueler.urls')),
    
    #Stammdaten
    url(r'^stammdaten/', include ('stammdaten.urls')),
    
    #theme.html, um sich Ideen zu holen
    url(r'^theme/', include ('theme.urls')),
    
    #Startpage
    url(r'^$', include ('home.urls')),
]
