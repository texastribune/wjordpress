from django.template import Context, Template

from . import WPTestCase
from ..factories import WPSiteFactory


class WidgetTestCase(WPTestCase):
    def test_wjidget_missing_site_raises_exception(self):
        t = Template('{% load wjidget from wjordpress %}{% wjidget "foo" %}')
        # TODO ImproperlyConfigured should be raised
        with self.assertRaises(Exception):
            t.render(Context())

    def test_wjidget_renders(self):
        WPSiteFactory(name='foo')
        t = Template('{% load wjidget from wjordpress %}{% wjidget "foo" %}')
        output = t.render(Context())
        self.assertIn('wjordpress-widget', output)
