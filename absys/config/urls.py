# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    url(r'^passwort_aendern/$', auth_views.PasswordChangeView.as_view(), {'post_change_redirect': '/'},
        name='absys_passwort_aendern'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^anwesenheitsliste/', include('absys.apps.anwesenheitsliste.urls')),
    url(r'^abrechnung/', include('absys.apps.abrechnung.urls')),
    url(r'^benachrichtigungen/', include('absys.apps.benachrichtigungen.urls')),
    url(r'^login/$', auth_views.LoginView.as_view(),
        {'template_name': 'anmeldung/templates/anmeldung/login.html'}, name='absys_login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('dashboard_dashboard')}, name='absys_logout'),
    url(r'^', include('absys.apps.dashboard.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
