from django.contrib import admin

from . import models


class WPSiteAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'description')

    def save_model(self, request, obj, form, change):
        # TODO do this sync async (give celery another shot?)
        obj.save()
        obj.sync()
admin.site.register(models.WPSite, WPSiteAdmin)


class WPPostAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.WPPost, WPPostAdmin)
