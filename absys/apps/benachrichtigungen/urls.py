from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.BenachrichtigungListView.as_view(),
        name='benachrichtigungen_benachrichtigung_list'
    ),
]
