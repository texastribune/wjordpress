from django.conf.urls import patterns, include, url
from django.http import HttpResponse

from django.contrib import admin
admin.autodiscover()


def favicon(request):
    """Hack to keep logs from filling with favicon.ico requests."""
    image_data = open("example_project/static/favicon.ico", "rb").read()
    return HttpResponse(image_data, mimetype="image/x-icon")


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('wjordpress.urls',
        namespace='wjordpress', app_name='wjordpress')),

    # HACK patterns
    url(r'^favicon.ico$', favicon),
)
