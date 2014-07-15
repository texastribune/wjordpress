"""

field names are taken to match the json output (except always lowercase). This
includes `id`. For the true primary key, use the `pk` attribute. But hey, you
were already doing that, right? This makes it so that matching fields between
the Django models and the JSON resource always match.

`max_length`s of 255 means I just picked an arbitrary high number and does not
reflect some real schema limit.
"""
from django.db import models

from . import managers
from .api import WPApi


class WPObjectModel(models.Model):
    dj_id = models.AutoField(primary_key=True)
    wp = models.ForeignKey('WPSite')
    id = models.PositiveIntegerField()

    synced_at = models.DateTimeField(null=True, blank=True)  # TODO

    class Meta:
        abstract = True
        unique_together = ('wp', 'id')


class WPSite(models.Model):
    url = models.URLField('URL', unique=True,
        help_text=u'The URL of the WordPress site.')
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = u'site'

    def __unicode__(self):
        return self.name or self.url

    def get_absolute_url(self):
        return self.url

    # CUSTOM METHODS #

    def fetch(self):
        api = WPApi(self.url)
        self.save_from_resource(api.index())

    def save_from_resource(self, data):
        self.name = data['name']
        self.description = data['description']
        self.save()

    def sync(self):
        api = WPApi(self.url)
        self.save_from_resource(api.index())
        data = api.posts()
        WPPost.objects.get_or_create_from_resource_list(self, data)


class WPAuthor(WPObjectModel):
    slug = models.SlugField(max_length=255)
    url = models.URLField(null=True, blank=True,
        help_text='The url the author has set as their homepage.')
    name = models.CharField(max_length=255)
    avatar = models.URLField(null=True, blank=True)
    # first_name
    # last_name

    objects = managers.WPAuthorManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url


class WPPost(WPObjectModel):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)  # choices? `publish`
    type = models.CharField(max_length=255)  # choices? `post`
    content = models.TextField(null=True, blank=True)
    link = models.URLField()
    date = models.DateTimeField()
    modified = models.DateTimeField()
    slug = models.SlugField(max_length=255)
    excerpt = models.TextField(null=True, blank=True)

    objects = managers.WPPostManager()

    class Meta(WPObjectModel.Meta):
        verbose_name = u'post'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link


class WPTag(WPObjectModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    link = models.URLField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.link


class WPCategory(WPObjectModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.link
