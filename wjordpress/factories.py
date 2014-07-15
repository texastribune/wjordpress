import factory

from django.utils.timezone import now

from .models import (
    WPSite,
    WPPost,
)


__all__ = ['WPSiteFactory', 'WPPostFactory']


class WPSiteFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WPSite

    url = factory.Sequence(lambda i: 'http://{}.sux'.format(i))


class WPPostFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WPPost

    wp = factory.SubFactory(WPSiteFactory)
    id = factory.Sequence(int)
    synced_at = factory.LazyAttribute(lambda __: now())
    date = factory.LazyAttribute(lambda __: now())
    modified = factory.LazyAttribute(lambda __: now())
