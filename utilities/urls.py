from django.conf.urls import url

from utilities.views import index, logout

urlpatterns = [
    url(r'^$', index, name='index'),
]