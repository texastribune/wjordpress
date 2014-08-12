from django.template import Context, Template

from . import WPTestCase


class WidgetTestCase(WPTestCase):
    def test_wjidget_works(self):
        t = Template('{% load wjidget from wjordpress %}')
        c = Context()
        output = t.render(c)
        print output
