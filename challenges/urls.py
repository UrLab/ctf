from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.list_challenges, name='challenge_list'),
    url(r'^archives/$', views.archives, name='challenge_archives'),
    url(r'^(?P<pk>[0-9]+)/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^(?P<pk>[0-9]+)/flag$', views.flag, name='flag'),
]
