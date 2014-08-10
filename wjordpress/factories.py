import factory

from django.utils.timezone import now

from .models import (
    WPSite,
    WPUser,
    WPTag,
    WPCategory,
    WPPost,
)


__all__ = ['WPSiteFactory', 'WPPostFactory']


class WPSiteFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WPSite

    url = factory.Sequence(lambda i: 'http://{}.site'.format(i))


class WPUserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WPUser

    wp = factory.SubFactory(WPSiteFactory)
    id = factory.Sequence(int)
    synced_at = factory.LazyAttribute(lambda __: now())
    url = factory.Sequence(lambda i: 'http://{}.user'.format(i))


class WPTagFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WPTag

    wp = factory.SubFactory(WPSiteFactory)
    id = factory.Sequence(int)
    synced_at = factory.LazyAttribute(lambda __: now())
    link = factory.Sequence(lambda i: 'http://{}.link'.format(i))


class WPCategoryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WPCategory

    wp = factory.SubFactory(WPSiteFactory)
    id = factory.Sequence(int)
    synced_at = factory.LazyAttribute(lambda __: now())
    link = factory.Sequence(lambda i: 'http://{}.link'.format(i))


class WPPostFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WPPost

    wp = factory.SubFactory(WPSiteFactory)
    id = factory.Sequence(int)
    synced_at = factory.LazyAttribute(lambda __: now())
    date = factory.LazyAttribute(lambda __: now())
    modified = factory.LazyAttribute(lambda __: now())
    link = factory.Sequence(lambda i: 'http://{}.post'.format(i))
