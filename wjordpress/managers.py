from django.db import models
from django.utils.timezone import now

import logging


class WPManager(models.Manager):
    def get_or_create_from_resource(self, site, data):
        field_names = self.model._meta.get_all_field_names()
        obj_data = {k: v for k, v in data.items() if k in field_names}
        obj_data['synced_at'] = now()
        return self.get_or_create(wp=site, id=data['ID'], defaults=obj_data)


class WPPostManager(models.Manager):
    def get_or_create_from_resource(self, site, data):
        field_names = self.model._meta.get_all_field_names()
        wp_id = data.pop('ID')
        obj_data = {k: v for k, v in data.items() if k in field_names}
        obj_data['synced_at'] = now()
        if 'author' in data:
            from .models import WPUser  # avoid circular imports
            author, created = WPUser.objects.get_or_create_from_resource(
                site, data['author'])
            obj_data['author'] = author
        obj_data['author'] = author
        obj, created = self.get_or_create(wp=site, id=wp_id, defaults=obj_data)
        # add many-to-many relations
        category_data = data['terms']['category']
        if category_data:
            from .models import WPCategory  # avoid circular imports
            for cat_data in category_data:
                cat, __ = WPCategory.objects.get_or_create_from_resource(
                    site, cat_data)
            # TODO handle category removal
            obj.categories.add(cat)
        tags_data = data['terms'].get('post_tag')
        if tags_data:
            from .models import WPTag  # avoid circular imports
            for tag_data in tags_data:
                tag, __ = WPTag.objects.get_or_create_from_resource(
                    site, tag_data)
            # TODO handle tag removal
            obj.tags.add(tag)
        return obj, created

    def get_or_create_from_resource_list(self, site, data):
        logger = logging.getLogger(__name__)
        for post in data:
            logger.debug(self.get_or_create_from_resource(site, post))
