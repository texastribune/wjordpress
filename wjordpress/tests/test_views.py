import json
import os

from django.test.client import RequestFactory
import mock

from . import WPTestCase
from ..factories import WPSiteFactory
from ..models import WPPost, WPLog
from ..views import HookPressEndpoint


BASE_DIR = os.path.dirname(__file__)


class HookPressEndpointTest(WPTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = HookPressEndpoint()

    def test_post_works(self):
        site = WPSiteFactory(url='http://www.foo.com/')
        # assert the post we're about to make doesn't exist
        self.assertFalse(WPPost.objects.filter(wp=site, id=521).exists())
        # sample POST based on a RequestBin[requestb.in] test
        request = self.factory.post('/foo/', {
            'hook': 'save_post',
            'ID': '521',
            'guid': 'http://www.foo.com/?p=521',
        })
        data = json.load(open(os.path.join(BASE_DIR, 'support', 'posts_521.json')))
        with mock.patch('wjordpress.models.WPApi') as MockApi:
            # got to be a better syntax for this
            MockApi.return_value = mock.MagicMock(**{'posts.return_value': data})
            response = self.view.post(request, site.pk)
        self.assertEqual(response.status_code, 200)
        # assert this post now exists
        self.assertTrue(WPPost.objects.filter(wp=site, id=521).exists())

    def test_post_creates_log(self):
        # assert we started with no log entries
        self.assertEqual(WPLog.objects.count(), 0)
        site = WPSiteFactory(url='http://www.foo.com/')
        request = self.factory.post('/foo/', {
            'foo': 'bar',
        })
        response = self.view.post(request, site.pk)
        self.assertEqual(response.status_code, 200)
        # assert log entry was created
        self.assertTrue(WPLog.objects.count())
