"""
Helper to make api queries.

Only does GET requests for now.

This is a simple wrapper; apart from the initial api instance, this only passes
dicts and json around.

TODO move out here! or use someone else's Python SDK. I'm lazy.

docs: https://github.com/WP-API/WP-API/blob/master/docs/guides/getting-started.md
"""
import logging
import requests

logger = logging.getLogger(__name__)


class WPApiException(Exception):
    pass


class UserCannotReadException(WPApiException):
    """
    Http 401 for when api does not have the auth to read a resource.
    """
    _code = 'json_user_cannot_read'
    message = 'Sorry, you cannot read this post.'


class InvalidPostIDException(WPApiException):
    """
    Http 404 for when a post does not exist.
    """
    _code = 'json_post_invalid_id'
    message = 'Invalid post ID.'


class WPApi(object):
    _total = None
    _total_page = None

    def __init__(self, url):
        """
        Initiate connection to a site.

        Site must have the `json-rest-api` plugin installed.
        """
        self.base_url = url.rstrip('/')

    def interpret_header(self, response, header):
        """If the header value is an integer, cast it."""
        out = response.headers.get(header)
        if out is not None:
            return int(out)
        return out

    def get(self, *args):
        url = u'{}/wp-json/'.format(self.base_url) + u'/'.join(args)
        response = requests.get(url)
        if not response.ok:
            if response.status_code == 401:
                raise UserCannotReadException()
            raise WPApiException()
        self.response = response  # store last response as an attribute
        self._total = self.interpret_header(response, 'X-WP-Total')
        self._total_pages = self.interpret_header(response, 'X-WP-TotalPages')
        logger.info(u'get {}'.format(url), extra={
            'headers': response.headers,
            'status_code': response.status_code,
            'response_text': response.text,
            'elapsed': response.elapsed,
        })
        return response.json()

    def index(self):
        """
        Get information about the site.

        https://raw.githubusercontent.com/WP-API/WP-API/master/docs/schema.json
        """
        return self.get()

    def posts(self, wp_id=None):
        """
        Get a list of posts.

        To get
        TODO handle pagination via the headers

        docs: https://github.com/WP-API/WP-API/blob/master/docs/guides/working-with-posts.md
        """
        if wp_id is None:
            # get a collection
            return self.get('posts')
        else:
            return self.get('posts', unicode(wp_id))

    def users(self):
        """
        Get a list of users.
        """
        return self.get('users')
