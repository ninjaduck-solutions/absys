# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^anwesenheitsliste/', include('absys.apps.anwesenheitsliste.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
