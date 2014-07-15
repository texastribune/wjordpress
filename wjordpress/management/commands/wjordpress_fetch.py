from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Manually fetch contents.'
    args = '[url]'

    def handle(self, url=None, *args, **options):
        from wjordpress.models import WPSite
        if url is None:
            for site in WPSite.objects.all():
                print u'Fetching {}'.format(site)
                site.fetch_all()
        else:
            try:
                site = WPSite.objects.get(url=url)
                site.fetch_all()
            except WPSite.DoesNotExist:
                print u'Error: Must specify an existing site. Options:'
                for site in WPSite.objects.all():
                    print u'  * {}'.format(site.url)
