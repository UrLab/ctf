from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.RegistrationView.as_view(), name='register'),
    url(r'^team$', views.show_team, name='team'),
    url(r'^team/join$', views.join_team, name='join_team'),
    url(r'^team/reset-secret-url$', views.reset_team_secret, name='reset_team_secret'),
    url(r'^team/invite/(?P<secret_key>(\d|\w){10,})$', views.accept_invite, name='accept_invite'),
]
