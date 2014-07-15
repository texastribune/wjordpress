import json
import os

from django.test import TestCase

from ..factories import WPPostFactory


BASE_DIR = os.path.dirname(__file__)


class WPObjectModelTest(TestCase):
    def test_save_from_resource_works(self):
        # WISHLIST assert WPPostFactory.save_from_resource is from WPObjectModel
        post = WPPostFactory()
        self.assertFalse(post.title)

        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts_521.json')))
        with self.assertNumQueries(1):
            post.save_from_resource(data)
        self.assertTrue(post.title)
