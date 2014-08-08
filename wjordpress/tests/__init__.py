from django.db.models.signals import post_save
from django.test import TestCase

from ..models import WPPost

try:
    from example_project.content.signals import sync_post
    DISCONNECT_SIGNALS = True
except ImportError:
    DISCONNECT_SIGNALS = False


class WPTestCase(TestCase):
    """
    TestCase with common logic.

    The example project adds some evil stuff we don't care about. Make sure
    it's gone when we test.
    """
    @classmethod
    def setUpClass(cls):
        if DISCONNECT_SIGNALS:
            post_save.disconnect(sync_post, sender=WPPost)

    @classmethod
    def tearDownClass(cls):
        if DISCONNECT_SIGNALS:
            post_save.connect(sync_post, sender=WPPost)

