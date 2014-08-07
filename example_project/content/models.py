from django.db import models
from django.db.models.signals import post_save
from wjordpress.models import WPPost

from .signals import sync_post


class Post(models.Model):
    headline = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    pub_status = models.CharField(max_length=1, default='D', choices=(
        ('D', 'Draft'),
        ('P', 'Published'),
        ('T', 'Trash'),
    ))
    pub_date = models.DateTimeField()
    text = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    # for wjordpress integration
    wppost = models.ForeignKey(WPPost, null=True, blank=True, related_name='+',
        unique=True, verbose_name='Original WP Post')

    class Meta:
        ordering = ('-pub_date', )

    def __unicode__(self):
        return self.headline

post_save.connect(sync_post, sender=WPPost)
