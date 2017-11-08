from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('utilities.urls')),
    url(r'^cards/', include('cards.urls')),
    url(r'^admin/', admin.site.urls),
]
