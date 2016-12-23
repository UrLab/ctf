from django.conf.urls import url, include
from django.contrib import admin
from . import views
import users.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^challenges/', include('challenges.urls')),
    url(r'scoreboard/', views.scoreboard, name="scoreboard"),
    url(r'^$', views.home, name="home"),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/register/$', users.views.register_new_user, name='register'),
    url(r'^accounts/team$', users.views.show_team, name='team'),
    url(r'^accounts/team/join$', users.views.join_team, name='join_team'),
    url(r'^accounts/team/reset-secret-url$', users.views.reset_team_secret, name='reset_team_secret'),
    url(r'^accounts/team/invite/(?P<secret_key>(\d|\w){10,})$', users.views.accept_invite, name='accept_invite'),
]
