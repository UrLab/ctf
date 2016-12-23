from django.conf.urls import url, include
from django.contrib import admin
from . import views
import users.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^challenges/', include('challenges.urls')),
    url(r'scoreboard/', views.scoreboard, name="scoreboard"),
    url(r'^$', views.home, name="home"),
    url('^', include('django.contrib.auth.urls')),
    url(r'^register/$', users.views.register_new_user, name='register'),
]
