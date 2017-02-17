from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^challenges/', include('challenges.urls')),
    url(r'scoreboard/', views.scoreboard, name="scoreboard"),
    url(r'stats/', views.stats, name="stats"),
    url(r'rules/', views.rules, name="rules"),
    url(r'^$', views.home, name="home"),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^accounts/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
