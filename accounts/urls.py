from django.conf.urls import url, include
from django.contrib.auth.views import logout

from accounts.views import login

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
]