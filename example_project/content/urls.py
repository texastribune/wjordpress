from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.PostList.as_view(), name='post_list'),
    url(r'^(?P<slug>[\-\w]+)/$', views.PostDetail.as_view(), name='post_detail'),
)
