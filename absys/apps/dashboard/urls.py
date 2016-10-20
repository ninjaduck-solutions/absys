# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^', views.DashboardView.as_view(), name='dashboard_dashboard'),
    ]