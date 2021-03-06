from django.conf import settings
from django.urls import include
from django.conf.urls import  url
from django.conf.urls.static import static
from django.contrib import admin

from newsletter.views import ( contact )
from matchmaker.views import about
from questions import views
from profiles.views import ( profile_view , job_create , job_edit , profile , profile_edit )
from likes.views import like_unlike_view
from dashboard.views import home
urlpatterns = [
    # Examples:
    url(r'^$', home, name='home'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^about/$', about , name='about'),
    url(r'^question/$', views.home,name='question'),
    url(r'^question/(?P<id>\d+)/$', views.single,name='question_single'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/$', profile , name='user_profile'),
    url(r'^profile/edit/$', profile_edit , name='edit_profile'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', profile_view , name='profile'),
    url(r'^jobs/add/$',job_create,name='job_add'),
    url(r'^jobs/edit/$',job_edit,name='job_edit'),
    url(r'^like/(?P<id>\d+)/$',like_unlike_view,name='like_unlike'),
    url(r'^matches/',include('matches.urls'))
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)