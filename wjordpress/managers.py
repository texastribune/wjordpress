from django.db import models
from django.utils.timezone import now


class WPUserManager(models.Manager):
    def get_or_create_from_resource(self, site, data):
        field_names = self.model._meta.get_all_field_names()
        wp_id = data.pop('ID')
        obj_data = {k: v for k, v in data.items() if k in field_names}
        obj_data['synced_at'] = now()
        return self.get_or_create(wp=site, id=wp_id, defaults=obj_data)


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
        return self.get_or_create(wp=site, id=wp_id, defaults=obj_data)

    def get_or_create_from_resource_list(self, site, data):
        for post in data:
            self.get_or_create_from_resource(site, post)
