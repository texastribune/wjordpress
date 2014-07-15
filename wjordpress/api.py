"""
Helper to make api queries.

Only does GET requests for now.

This is a simple wrapper; apart from the initial api instance, this only passes
dicts and json around.

TODO move out here! or use someone else's Python SDK. I'm lazy.
"""
import requests


class WPApi(object):
    def __init__(self, url):
        """
        Initiate connection to a site.

        Site must have the `json-rest-api` plugin installed.
        """
        self.base_url = url.rstrip('/')

    def get(self, *args):
        url = '{}/wp-json/'.format(self.base_url) + '/'.join(args)
        response = requests.get(url)
        self.response = response  # store last response as an attribute
        return response.json()

    def index(self):
        """
        Get information about the site.

        https://raw.githubusercontent.com/WP-API/WP-API/master/docs/schema.json
        """
        return self.get()

    def posts(self):
        """
        Get a list of posts.

        TODO handle pagination via the headers
        """
        return self.get('posts')

    def users(self):
        """
        Get a list of users.
        """
        return self.get('users')

