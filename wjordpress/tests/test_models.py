import json
import mock
import os

from . import WPTestCase
from ..factories import (
    WPSiteFactory, WPUserFactory, WPTagFactory, WPCategoryFactory,
    WPPostFactory,
)
from ..models import WPLog


BASE_DIR = os.path.dirname(__file__)


class WPObjectModelTest(WPTestCase):
    def test_save_from_resource_works(self):
        # WISHLIST assert WPPostFactory.save_from_resource is from WPObjectModel
        post = WPPostFactory()
        self.assertFalse(post.title)

        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts_521.json')))
        with self.assertNumQueries(1):
            post.save_from_resource(data)
        self.assertTrue(post.title)


class WPSiteTest(WPTestCase):
    # not a very good test, should use real data
    mock_data = {
        'name': 'hello',
        'description': 'world',
    }

    def setUp(self):
        self.site = WPSiteFactory()
        super(WPTestCase, self).setUp()

    def test_get_absolute_url_works(self):
        self.assertTrue(self.site.get_absolute_url())

    def test_hook_url_works(self):
        self.assertTrue(self.site.hook_url)
        # like traditional get_absolute_url, is actually a path
        self.assertTrue(self.site.hook_url.startswith('/'))

    def test_save_from_resource_works(self):
        self.site.save_from_resource(self.mock_data)
        self.assertEqual(self.site.name, 'hello')
        self.assertEqual(self.site.description, 'world')

    def test_fetch_creates_log(self):
        # assert we started with no log entries
        self.assertEqual(WPLog.objects.count(), 0)
        with mock.patch('wjordpress.models.WPApi') as mock_api:
            mock_api.return_value = mock_api  # simplify the mock
            mock_api.index.return_value = self.mock_data
            self.site.fetch()
        # assert log entry was created
        self.assertTrue(WPLog.objects.count())

    def test_fetch_all_creates_log(self):
        # assert we started with no log entries
        self.assertEqual(WPLog.objects.count(), 0)
        with mock.patch('wjordpress.models.WPApi') as mock_api:
            mock_api.return_value = mock_api  # simplify the mock
            mock_api.index.return_value = self.mock_data
            mock_api.posts.return_value = []
            self.site.fetch_all()
        # assert log entry was created
        self.assertTrue(WPLog.objects.count())


class WPUserTest(WPTestCase):
    def test_get_absolute_url_works(self):
        user = WPUserFactory()
        self.assertTrue(user.get_absolute_url())


class WPTagTest(WPTestCase):
    def test_get_absolute_url_works(self):
        tag = WPTagFactory()
        self.assertTrue(tag.get_absolute_url())


class WPCategoryTest(WPTestCase):
    def test_get_absolute_url_works(self):
        category = WPCategoryFactory()
        self.assertTrue(category.get_absolute_url())


class WPPostTest(WPTestCase):
    def test_get_absolute_url_works(self):
        post = WPPostFactory()
        self.assertTrue(post.get_absolute_url())

    def test_images_works(self):
        # assert if post has no meta, it has no images
        post = WPPostFactory()
        self.assertIsNone(post.images)
