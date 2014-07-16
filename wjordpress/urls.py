from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^hook/(?P<pk>\d+)/$', views.HookPressEndpoint.as_view(),
        name=u'hook_endpoint'),
)
