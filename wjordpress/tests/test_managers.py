import json
import os

from django.test import TestCase

from ..factories import WPSiteFactory
from ..managers import WPPostManager
from ..models import WPUser, WPTag, WPCategory, WPPost


BASE_DIR = os.path.dirname(__file__)


class WPPostManagerTest(TestCase):
    def test_it_works(self):
        self.assertIsInstance(WPPost.objects, WPPostManager)
        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts.json')))
        site = WPSiteFactory()
        with self.assertNumQueries(170):
            WPPost.objects.get_or_create_from_resource_list(site, data)
        # assert 8 posts were created
        self.assertEqual(WPPost.objects.count(), 8)
        # assert 1 user was created
        self.assertEqual(WPUser.objects.count(), 1)
        # assert 7 categories were created
        self.assertEqual(WPCategory.objects.count(), 7)
        # assert 7 tags were created
        self.assertEqual(WPTag.objects.count(), 14)
