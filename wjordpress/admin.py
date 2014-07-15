from django.contrib import admin

from . import models


class WPSiteAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'description')

    def save_model(self, request, obj, form, change):
        # TODO do this sync async (give celery another shot?)
        obj.save()
        obj.fetch_all()
admin.site.register(models.WPSite, WPSiteAdmin)


class WPUserAdmin(admin.ModelAdmin):
    readonly_fields = ('synced_at', )
admin.site.register(models.WPUser, WPUserAdmin)


class WPCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('synced_at', )
admin.site.register(models.WPCategory, WPCategoryAdmin)


class WPTagAdmin(admin.ModelAdmin):
    readonly_fields = ('synced_at', )
admin.site.register(models.WPTag, WPTagAdmin)


class WPPostAdmin(admin.ModelAdmin):
    readonly_fields = ('synced_at', )
admin.site.register(models.WPPost, WPPostAdmin)
