from django.conf.urls import url

from utilities.views import index

urlpatterns = [
    url(r'^$', index, name='index'),
]