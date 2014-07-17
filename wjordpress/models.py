"""

field names are taken to match the json output (except always lowercase). This
includes `id`. For the true primary key, use the `pk` attribute. But hey, you
were already doing that, right? This makes it so that matching fields between
the Django models and the JSON resource always match.

`max_length`s of 255 means I just picked an arbitrary high number and does not
reflect some real schema limit.
"""
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now

from . import managers
from .api import WPApi


###################
# ABSTRACT MODELS #
###################

class WPObjectModel(models.Model):
    wp = models.ForeignKey('WPSite')
    id = models.PositiveIntegerField()

    # bookkeepping
    dj_id = models.AutoField(primary_key=True)
    synced_at = models.DateTimeField()  # don't use auto_now for future
                                        # `bulk_insert` compatibility

    class Meta:
        abstract = True
        unique_together = ('wp', 'id')

    # CUSTOM METHODS #
    def fetch(self):
        """
        Fetch this object from the api and update.
        """
        raise NotImplementedError

    def save_from_resource(self, data):
        """
        Takes the data from the api and applies it back to the instance.

        Similar to `WPManager.get_or_create_from_resource`.
        """
        field_names = self._meta.get_all_field_names()
        obj_data = {k: v for k, v in data.items() if k in field_names}
        obj_data['synced_at'] = now()
        # WISHLIST log what changed
        self.__dict__.update(obj_data)
        self.save()


##########
# MODELS #
##########

class WPSite(models.Model):
    """
    This describes the WordPress site you're trying to integrate with.

    We only need the url.
    """
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

    # CUSTOM PROPERTIES #

    @property
    def hook_url(self):
        return reverse('wjordpress:hook_endpoint', kwargs={'pk': self.pk})

    # CUSTOM METHODS #

    def save_from_resource(self, data):
        self.name = data['name']
        self.description = data['description']
        self.save()

    def fetch(self):
        api = WPApi(self.url)
        self.save_from_resource(api.index())

    def fetch_all(self):
        api = WPApi(self.url)
        self.save_from_resource(api.index())
        data = api.posts()
        WPPost.objects.get_or_create_from_resource_list(self, data)


class WPUser(WPObjectModel):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    url = models.URLField(null=True, blank=True,
        help_text='The url the author has set as their homepage.')
    avatar = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    registered = models.DateTimeField(null=True, blank=True)
    # first_name
    # last_name

    # MANAGERS #
    objects = managers.WPManager()

    class Meta(WPObjectModel.Meta):
        verbose_name = u'user'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url


class WPTag(WPObjectModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    link = models.URLField()

    # MANAGERS #
    objects = managers.WPManager()

    class Meta(WPObjectModel.Meta):
        verbose_name = u'tag'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.link


class WPCategory(WPObjectModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()

    # MANAGERS #
    objects = managers.WPManager()

    class Meta(WPObjectModel.Meta):
        verbose_name = u'category'
        verbose_name_plural = u'categories'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.link


class WPPost(WPObjectModel):
    """
    WordPress Posts. This is the main content type.

    more about revisions: http://codex.wordpress.org/Revisions
    """
    title = models.CharField(max_length=255)
    # http://codex.wordpress.org/Post_Status
    status = models.CharField(max_length=20, choices=(
        ('publish', 'Published'),
        ('future', 'Future'),
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('private', 'Private'),
        ('trash', 'Trash'),
        ('auto-draft', 'Auto-Draft'),
        ('inherit', 'Inherit'),
    ))
    # http://codex.wordpress.org/Post_Types
    type = models.CharField(max_length=20, choices=(
        ('post', 'Post'),
        ('page', 'Page'),
        ('attachment', 'Attachment'),
        ('revision', 'Revision'),
        ('nav_menu_item', 'Navication menu'),
    ))  # choices? `post`
    content = models.TextField(null=True, blank=True)
    link = models.URLField()
    date = models.DateTimeField()
    modified = models.DateTimeField()
    slug = models.SlugField(max_length=255)
    excerpt = models.TextField(null=True, blank=True)

    author = models.ForeignKey(WPUser, null=True, blank=True)
    categories = models.ManyToManyField(WPCategory)
    tags = models.ManyToManyField(WPTag)

    parent = models.ForeignKey('self', null=True, blank=True,
        related_name='revisions',
        help_text=u'Revision parent.')

    # MANAGERS #
    objects = managers.WPPostManager()

    class Meta(WPObjectModel.Meta):
        get_latest_by = 'date'
        ordering = ('-date', )
        verbose_name = u'post'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link

    # `WPObjectModel` METHODS #
    def fetch(self):
        api = WPApi(self.wp.url)
        data = api.posts(self.id)
        self.save_from_resource(data)
