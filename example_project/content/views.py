from django.views.generic import ListView, DetailView

from .models import Post


class PostList(ListView):
    queryset = Post.objects.filter(pub_status='P')


class PostDetail(DetailView):
    queryset = Post.objects.filter(pub_status='P')
