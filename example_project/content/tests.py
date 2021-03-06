"""
Ancillary tests, not distributed in the package.

Just to make sure this content syncing stuff works. Really quick n' dirty.

You can run these tests with:

     django test example_project.content.tests
"""
import json
import os

from django.test import TestCase
from wjordpress.factories import WPSiteFactory
from wjordpress.models import WPPost

from .models import Post, RemoteImage


BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'wjordpress', 'tests')


class ItWorks(TestCase):
    def test_get_or_create_from_resource_list_works(self):
        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts.json')))
        site = WPSiteFactory()
        WPPost.objects.get_or_create_from_resource_list(site, data)
        # assert posts were created
        self.assertEqual(WPPost.objects.count(), 9)

        self.assertEqual(Post.objects.count(), 8)
        self.assertEqual(RemoteImage.objects.count(), 1)

        image = RemoteImage.objects.get()
        # assert the image is associated with a post
        self.assertEqual(image.post_set.count(), 1)

        # make sure updating works
        wppost = WPPost.objects.latest('date')
        post = Post.objects.get(wppost=wppost)
        self.assertNotEqual(post.headline, 'foo')
        wppost.title = 'foo'
        wppost.save()
        post = Post.objects.get(wppost=wppost)
        self.assertEqual(post.headline, 'foo')
