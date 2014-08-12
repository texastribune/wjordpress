from django import template

from ..models import WPSite, WPPost


register = template.Library()


@register.inclusion_tag('wjordpress/widget.html')
def wjidget(wp_site_name, limit=10):
    """
    This renders a widget you can use to quickly show wordpress content.

    Pass in the name of the wordpress site.
    TODO the name of the site is a brittle way to reference, but it seems more
    human friendly than the url.
    """
    wp_site = WPSite.objects.get(name=wp_site_name)
    return {
        'object_list': WPPost.objects.filter(
            wp=wp_site,
            status='publish',  # XXX magic constant
            type='post',  # XXX magic constant
        )[:limit],
    }
