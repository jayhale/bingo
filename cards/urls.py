from django.conf.urls import url, include

from cards.views import index, card

urlpatterns = [
    url(r'^$', index, name='cards'),
    url(r'^(?P<week_pk>[0-9]+)/$', card, name='card'),
]