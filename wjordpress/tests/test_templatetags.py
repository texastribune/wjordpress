from django.template import Context, Template

from . import WPTestCase
from ..factories import WPSiteFactory, WPPostFactory


class WidgetTestCase(WPTestCase):
    def test_wjidget_missing_site_raises_exception(self):
        t = Template('{% load wjidget from wjordpress %}{% wjidget "foo" %}')
        # TODO ImproperlyConfigured should be raised
        with self.assertRaises(Exception):
            t.render(Context())

    def test_wjidget_renders(self):
        num_posts = 3  # XXX this is less than the default limit
        wp_site = WPSiteFactory(name='foo')
        for i in range(num_posts):
            WPPostFactory(
                wp=wp_site,
                type='post',
                status='publish',
                title='{}'.format(i),
                excerpt='{}'.format(i),
            )
        t = Template('{% load wjidget from wjordpress %}{% wjidget "foo" %}')
        output = t.render(Context())
        self.assertIn('wjidget-container', output)
        self.assertEqual(output.count('<article>'), num_posts)

    def test_wjidget_can_be_limited(self):
        wp_site = WPSiteFactory(name='foo')
        for i in range(11):
            WPPostFactory(
                wp=wp_site,
                type='post',
                status='publish',
                title='{}'.format(i),
                excerpt='{}'.format(i),
            )
        t = Template('{% load wjidget from wjordpress %}'
            '{% wjidget "foo" limit=5 %}')
        output = t.render(Context())
        self.assertEqual(output.count('<article>'), 5)
