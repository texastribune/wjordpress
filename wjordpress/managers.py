from django.db import models
from django.utils.timezone import now

import logging


class WPManager(models.Manager):
    def get_or_create_from_resource(self, site, data):
        """
        Get or create an instance based on the json.
        """
        field_names = self.model._meta.get_all_field_names()
        obj_data = {k: v for k, v in data.items() if k in field_names}
        obj_data['synced_at'] = now()
        return self.get_or_create(wp=site, id=data['ID'], defaults=obj_data)

    def get_or_create_from_resource_list(self, site, data):
        """
        Get or create multiples from an array json.
        """
        logger = logging.getLogger(__name__)
        for datum in data:
            logger.debug(self.get_or_create_from_resource(site, datum))


class WPPostManager(WPManager):
    def get_or_create_from_resource(self, site, data):
        """
        Get or create an instance based on the json.

        The `WPPost` object has some relations that need to be handled special.
        """
        if 'author' in data:
            from .models import WPUser  # avoid circular imports
            author, __ = WPUser.objects.get_or_create_from_resource(
                site, data['author'])
            data['author'] = author  # XXX mutate original `data` to reference
                                     # something else. I should have made a
                                     # copy, but I'm lazy
        # 'parent' is either `0` or another post json or an int
        parent_data = data.pop('parent')
        if parent_data:
            if isinstance(parent_data, int):
                data['parent'] = self.model.objects.get(wp=site, id=parent_data)
            else:
                # may need to catch DoesNotExist
                data['parent'] = self.model.objects.get(wp=site, id=parent_data['ID'])
        # 'featured_image' isn't always in the resource JSON
        featured_image_data = data.pop('featured_image') if 'featured_image' in data else None

        obj, created = (super(WPPostManager, self)
            .get_or_create_from_resource(site, data))

        if featured_image_data is not None:
            # featured_image_data references the post, so this has to happen
            # after the post is created
            # TODO need to store that this is an image and attachment_meta
            featured_image, __ = self.get_or_create_from_resource(site, featured_image_data)
            # mutate the data to shim `original` into the `sizes` dict
            featured_image_data['attachment_meta']['sizes']['original'] = {
                'file': featured_image_data['attachment_meta']['file'],
                'width': featured_image_data['attachment_meta']['width'],
                'height': featured_image_data['attachment_meta']['height'],
                'mime-type': 'image/jpeg',  # FIXME where do we get this?
                'url': featured_image_data['source'],
            }
            obj.featured_image = featured_image
            obj.save()
        # add many-to-many relations
        if data['terms']:
            category_data = data['terms'].get('category')
            if category_data:
                from .models import WPCategory  # avoid circular imports
                # TODO handle category removal
                for cat_data in category_data:
                    cat, __ = WPCategory.objects.get_or_create_from_resource(
                        site, cat_data)
                    obj.categories.add(cat)
            tags_data = data['terms'].get('post_tag')
            if tags_data:
                from .models import WPTag  # avoid circular imports
                # TODO handle tag removal
                for tag_data in tags_data:
                    tag, __ = WPTag.objects.get_or_create_from_resource(
                        site, tag_data)
                    obj.tags.add(tag)
        return obj, created


class WPLogManager(models.Manager):
    def push(self, wp, action, body=u''):
        """Generic way to create a log entry."""
        if not wp.enable_log:
            return
        self.create(wp=wp, action=action, body=body)
