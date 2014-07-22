import json
import os

from django.test import TestCase

from ..factories import WPSiteFactory, WPPostFactory
from ..managers import WPPostManager
from ..models import WPUser, WPTag, WPCategory, WPPost


BASE_DIR = os.path.dirname(__file__)


class WPPostManagerTest(TestCase):
    def test_get_or_create_from_resource_works(self):
        self.assertIsInstance(WPPost.objects, WPPostManager)
        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts_521.json')))
        site = WPSiteFactory()
        with self.assertNumQueries(28):
            post, created = WPPost.objects.get_or_create_from_resource(
                site, data)
        self.assertTrue(created)
        self.assertEqual(post.id, 521)
        self.assertEqual(post.author.id, 1)
        self.assertEqual(post.categories.count(), 1)
        self.assertEqual(post.tags.count(), 1)

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
        with self.assertNumQueries(35):
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
        with self.assertNumQueries(177):
            WPPost.objects.get_or_create_from_resource_list(site, data)
        # assert 8 posts were created
        self.assertEqual(WPPost.objects.count(), 9)
        # assert 1 user was created
        self.assertEqual(WPUser.objects.count(), 1)
        # assert 7 categories were created
        self.assertEqual(WPCategory.objects.count(), 7)
        # assert 7 tags were created
        self.assertEqual(WPTag.objects.count(), 14)
