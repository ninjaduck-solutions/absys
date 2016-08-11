from django.conf.urls import include, url

from django.contrib.auth.views import login, logout

urlpatterns = [
        url(r'^$', login, {'template_name': 'anmeldung/login.html'},
            name='login'),
        url(r'^abmelden/$', logout, {'next_page': '/'},
            name='logout'),
        # url(r'^passwort-aendern/$', 'password_change',
        #     {'template_name': 'userauth/password_change_form.html'},
        #     name='userauth_password_change'),
        # url(r'^passwort-geaendert/$', 'password_change_done',
        #     {'template_name': 'userauth/password_change_done.html'},
        #     name='userauth_password_change_done')
    ]