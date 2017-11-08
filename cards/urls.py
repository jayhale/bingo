from django.conf.urls import url, include

from cards.views import index, card

urlpatterns = [
    url(r'^(?P<user_pk>[0-9]+)/$', index, name='cards'),
    url(r'^(?P<user_pk>[0-9]+)/week/(?P<week_pk>[0-9]+)/$', card, name='card'),
]