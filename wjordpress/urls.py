from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^hook/$', views.HookPressEndpoint.as_view(),
        name=u'hook_endpoint'),
)
