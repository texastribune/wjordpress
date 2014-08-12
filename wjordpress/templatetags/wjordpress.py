from django import template

from ..models import WPSite, WPPost


register = template.Library()


@register.inclusion_tag('wjordpress/widget.html')
def wjidget(wp_site_name):
    """
    This renders a widget you can use to quickly show wordpress content.
    """
    wp_site = WPSite.objects.get(name=wp_site_name)
    return WPPost.objects.filter(wp=wp_site, status='publish')
