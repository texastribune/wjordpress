import factory

from .models import (
    WPSite,
)


class WPSiteFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WPSite

    url = factory.Sequence(lambda i: 'http://{}.sux'.format(i))
