from django.conf.urls import url, include

from cards.views import index, card, winner

urlpatterns = [
    url(r'^$', index, name='cards'),
    url(r'^(?P<week_pk>[0-9]+)/$', card, name='card'),
    url(r'^(?P<week_pk>[0-9]+)/winner/$', winner, name='winner'),
]