from django.views.generic import ListView, DetailView

from wjordpress.models import WPSite, WPPost


class NavbarMixin(object):
    def all_sites(self):
        return WPSite.objects.all()


class PostList(NavbarMixin, ListView):
    template_name = 'list.html'
    model = WPPost


class PostDetail(NavbarMixin, DetailView):
    template_name = 'detail.html'
    model = WPPost
