from django.db import models


class WPAuthorManager(models.Manager):
    def get_or_create_from_resource(self, data):
        pass


class WPPostManager(models.Manager):
    def get_or_create_from_resource(self, site, data):
        field_names = self.model._meta.get_all_field_names()
        wp_id = data.pop('ID')
        obj_data = {k: v for k, v in data.items() if k in field_names}
        return self.get_or_create(wp=site, id=wp_id, defaults=obj_data)

    def get_or_create_from_resource_list(self, site, data):
        for post in data:
            self.get_or_create_from_resource(site, post)
