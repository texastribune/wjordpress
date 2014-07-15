"""

field names are taken to match the json output (except always lowercase).

`id` field is explicitly added when an `id` field is given from the api.

`max_length`s of 255 means I just picked an arbitrary high number and does not
reflect some real schema limit.
"""
from django.db import models


class WPSite(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name or self.url

    def get_absolute_url(self):
        return self.url


class WPAuthor(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    slug = models.SlugField(max_length=255)
    url = models.URLField(null=True, blank=True,
        help_text='The url the author has set as their homepage.')
    name = models.CharField(max_length=255)
    avatar = models.URLField(null=True, blank=True)
    # first_name
    # last_name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url


class WPPost(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)  # choices? `publish`
    type = models.CharField(max_length=255)  # choices? `post`
    content = models.TextField(null=True, blank=True)
    link = models.URLField()
    date = models.DateTimeField()
    modified = models.DateTimeField()
    slug = models.SlugField(max_length=255)
    excerpt = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link


class WPTag(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    link = models.URLField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.link


class WPCategory(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.link
