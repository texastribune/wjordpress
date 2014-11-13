from __future__ import unicode_literals

import json
import os

from . import WPTestCase
from ..factories import WPSiteFactory, WPPostFactory
from ..managers import WPManager, WPPostManager, WPLogManager
from ..models import WPUser, WPTag, WPCategory, WPPost, WPLog

BASE_DIR = os.path.dirname(__file__)


class WPManagerTest(WPTestCase):
    def test_get_or_create_from_resource_works(self):
        # setup
        site = WPSiteFactory()
        # sanity check
        self.assertIsInstance(WPUser.objects, WPManager)
        data = {
            'ID': 1337,
            'username': 'gregor',
            'slug': 'admin',
            'URL': 'http://metamorphos.is',
            'avatar': 'http://robohash.org/admin.png',
            'description': 'Definitely human',
            'registered': '2008-01-03T01:52:52+00:00',
            # 'first_name', 'last_name', 'nickname', 'meta'
        }
        user, created = WPUser.objects.get_or_create_from_resource(site, data)
        self.assertTrue(created)
        self.assertEqual(user.id, 1337)
        self.assertEqual(user.username, 'gregor')

        data['username'] = 'samsa'
        user, created = WPUser.objects.get_or_create_from_resource(site, data)
        self.assertFalse(created)
        self.assertEqual(user.id, 1337)
        self.assertEqual(user.username, 'samsa')


class WPPostManagerTest(WPTestCase):
    def test_get_or_create_from_resource_works(self):
        # sanity check
        self.assertIsInstance(WPPost.objects, WPPostManager)
        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts_521.json')))
        site = WPSiteFactory()
        with self.assertNumQueries(32):
            post, created = WPPost.objects.get_or_create_from_resource(
                site, data)
        self.assertTrue(created)
        self.assertEqual(post.id, 521)
        self.assertEqual(post.author.id, 1)
        self.assertEqual(post.categories.count(), 2)
        self.assertEqual(post.tags.count(), 2)

    def test_get_or_create_from_resource_handles_revisions_and_parent(self):
        self.assertIsInstance(WPPost.objects, WPPostManager)
        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts_536.json')))
        site = WPSiteFactory()
        parent = WPPostFactory(wp=site, id=data['parent']['ID'])
        with self.assertNumQueries(9):
            post, created = WPPost.objects.get_or_create_from_resource(
                site, data)
        self.assertTrue(created)
        self.assertEqual(post.id, 536)
        self.assertEqual(post.parent, parent)

    def test_get_or_create_from_resource_handles_featured_image(self):
        self.assertIsInstance(WPPost.objects, WPPostManager)
        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts_502.json')))
        site = WPSiteFactory()
        with self.assertNumQueries(40):
            post, created = WPPost.objects.get_or_create_from_resource(
                site, data)
        self.assertTrue(created)
        self.assertEqual(post.id, 502)
        # assert post has a featured image
        self.assertTrue(post.featured_image)
        # assert the featured image has info
        self.assertEqual(post.featured_image.attachment_meta['width'], 1259)
        self.assertEqual(post.featured_image.attachment_meta['height'], 485)
        # assert the original was saved
        self.assertEqual(post.featured_image.images['original'].width, 1259)
        self.assertEqual(post.featured_image.images['original'].height, 485)
        # assert other sizes were saved
        self.assertIn('large', post.featured_image.images)
        self.assertIn('medium', post.featured_image.images)
        self.assertIn('thumbnail', post.featured_image.images)

    def test_get_or_create_from_resource_list_works(self):
        self.assertIsInstance(WPPost.objects, WPPostManager)
        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts.json')))
        site = WPSiteFactory()
        with self.assertNumQueries(236):
            WPPost.objects.get_or_create_from_resource_list(site, data)
        # assert posts were created
        self.assertEqual(WPPost.objects.count(), 9)
        # assert user was created
        self.assertEqual(WPUser.objects.count(), 1)
        # assert categories were created
        self.assertEqual(WPCategory.objects.count(), 7)
        # assert tags were created
        self.assertEqual(WPTag.objects.count(), 14)


class WPLogManagerTest(WPTestCase):
    def test_push_works(self):
        self.assertIsInstance(WPLog.objects, WPLogManager)
        self.assertEqual(WPLog.objects.count(), 0)
        wp_site = WPSiteFactory()
        with self.assertNumQueries(1):
            WPLog.objects.push(wp_site, 'test')
        # assert one log entry created
        self.assertEqual(WPLog.objects.count(), 1)
