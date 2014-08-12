from django import template

from ..models import WPSite, WPPost


register = template.Library()


@register.inclusion_tag('wjordpress/widget.html')
def wjidget(wp_site_name):
    wp_site = WPSite.objects.get(wp_site_name)
    return WPPost.objects.filter(wp=wp_site)
