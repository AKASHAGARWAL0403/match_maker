from django.conf import settings
from django.urls import include
from django.conf.urls import  url
from django.conf.urls.static import static

from .views import ( position_match_view, location_match_view , employer_match_view)


urlpatterns = [
    url(r'^position/(?P<slug>[\w-]+)/$', position_match_view , name='position_match'),
    url(r'^location/(?P<slug>[\w-]+)/$', location_match_view , name='location_match'),
    url(r'^employer/(?P<slug>[\w-]+)/$', employer_match_view , name='employer_match'),
]
