"""
Light Coverage for the API

Very light.
"""
import json
import mock

import responses

from . import WPTestCase
from ..api import WPApi, UserCannotReadException, WPApiException


class WPApiTest(WPTestCase):

    def test_init_base_url_does_not_have_trailing_slash(self):
        api = WPApi('http://foo.com/')
        self.assertEqual(api.base_url, 'http://foo.com')

        api = WPApi('http://foo.com')
        self.assertEqual(api.base_url, 'http://foo.com')

    def test_interpret_header_does_stuff(self):
        mock_response = mock.MagicMock()
        mock_response.headers = {'number': 4, 'numberish': '5'}
        api = WPApi('http://foo.com')
        self.assertEqual(api.interpret_header(mock_response, 'number'), 4)
        self.assertEqual(api.interpret_header(mock_response, 'numberish'), 5)
        self.assertEqual(api.interpret_header(mock_response, 'dne'), None)

    @responses.activate
    def test_get_does_stuff(self):
        responses.add(responses.GET, 'http://foo.com/wp-json/',
            body=json.dumps({'hello': 'there'}))
        api = WPApi('http://foo.com')
        data = api.get()
        self.assertEqual(data['hello'], 'there')

    @responses.activate
    def test_get_raises_except_when_401(self):
        responses.add(responses.GET, 'http://foo.com/wp-json/',
            status=401)
        api = WPApi('http://foo.com')
        with self.assertRaises(UserCannotReadException):
            api.get()

    @responses.activate
    def test_get_raises_except_when_500(self):
        responses.add(responses.GET, 'http://foo.com/wp-json/',
            status=500)
        api = WPApi('http://foo.com')
        with self.assertRaises(WPApiException):
            api.get()

    @responses.activate
    def test_index_does_stuff(self):
        responses.add(responses.GET, 'http://foo.com/wp-json/',
            body=json.dumps({'hello': 'there'}))
        api = WPApi('http://foo.com')
        data = api.index()
        self.assertEqual(data['hello'], 'there')

    @responses.activate
    def test_posts_does_stuff(self):
        responses.add(responses.GET, 'http://foo.com/wp-json/posts',
            body=json.dumps({'hello': 'there'}))
        api = WPApi('http://foo.com')
        data = api.posts()
        self.assertEqual(data['hello'], 'there')

    @responses.activate
    def test_posts_for_specific_post_does_stuff(self):
        responses.add(responses.GET, 'http://foo.com/wp-json/posts/1337',
            body=json.dumps({'hello': 'there'}))
        api = WPApi('http://foo.com')
        data = api.posts(1337)
        self.assertEqual(data['hello'], 'there')

    @responses.activate
    def test_users_does_stuff(self):
        responses.add(responses.GET, 'http://foo.com/wp-json/users',
            body=json.dumps({'hello': 'there'}))
        api = WPApi('http://foo.com')
        data = api.users()
        self.assertEqual(data['hello'], 'there')
