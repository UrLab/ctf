from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^challenges/', include('challenges.urls')),
    url(r'scoreboard/', views.scoreboard, name="scoreboard"),
    url(r'^$', views.home, name="home"),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^accounts/', include('users.urls')),
]
