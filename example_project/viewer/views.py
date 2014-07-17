from django.views.generic import ListView, DetailView

from wjordpress.models import WPSite, WPPost


class NavbarMixin(object):
    def all_sites(self):
        return WPSite.objects.all()


class PostList(NavbarMixin, ListView):
    template_name = 'list.html'
    queryset = WPPost.objects.filter(status='publish')


class PostDetail(NavbarMixin, DetailView):
    template_name = 'detail.html'
    queryset = WPPost.objects.filter(status='publish')
