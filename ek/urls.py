from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from apps.restapi.views import router

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'apps.guest.views.index', name='index'),
    url(r'^login/$', 'apps.guest.views.login', name='login'),
    url(r'^auth/$', 'apps.guest.views.auth', name='auth'),
    url(r'^logout/$', 'apps.guest.views.logout', name='logout'),
    url(r'^register/$', 'apps.guest.views.register_user', name='register_user'),

    url(r'^user/profile/$', 'apps.main.views.profile', name='profile'),
    url(r'^user/profile/(?P<user_id>\d+)/$', 'apps.main.views.profile', name='profile'),
    url(r'^tasks/$', 'apps.main.views.tasks', name='tasks_all'),
    url(r'^tasks/(?P<action>\w+)/$', 'apps.main.views.tasks', name='tasks'),
    url(r'^task/add/$', 'apps.main.views.task_add', name='task_add'),
    url(r'^task/(?P<task_id>\d+)/$', 'apps.main.views.task', name='task'),

    url(r'^news/$', 'apps.main.views.news', name='news'),
    url(r'^statistic/$', 'apps.main.views.statistic', name='statistic'),

    url(r'^addcomment/(?P<task_id>\d+)/$', 'apps.main.views.addcomment', name='addcomment'),

    url(r'^admin/', include(admin.site.urls)),

    #Added
    url(r'^add/percent/(?P<task_id>\d+)/$', 'apps.main.views.add_percent', name='add_percent'),
    
    url(r'^map/$', 'apps.main.views.map', name='map'),
    url(r'^map/(?P<action>\w+)/$', 'apps.main.views.map', name='map'),
    url(r'^json/geopoints/$', 'apps.main.json_sender.send_all_geo_points'),
    url(r'^json/geopoints/(?P<action>\w+)/$', 'apps.main.json_sender.send_all_geo_points'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)