from django.contrib import admin

from . import models


class WPSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'hook')
    readonly_fields = ('name', 'description')

    def save_model(self, request, obj, form, change):
        # TODO do this sync async (give celery another shot?)
        obj.save()
        obj.fetch_all()

    # CUSTOM METHODS #

    def hook(self, obj):
        """
        This is where an admin can find what url to point the webhook to.

        Doing it as an absolute url lets us cheat and make the browser figure
        out the host for us.

        Requires HookPress: http://wordpress.org/plugins/hookpress/
        """
        return (u'<a href="{}" title="Add a save_post hook with the ID">'
            'Webhook</a>'.format(obj.hook_url))
    hook.allow_tags = True
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
    list_display = ('title', 'date', 'type', 'status', )
    list_filter = ('type', 'status', )
    readonly_fields = ('synced_at', )
admin.site.register(models.WPPost, WPPostAdmin)


class WPLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'wp', 'action', )
    list_filter = ('wp', 'action', )
    readonly_fields = ('wp', 'timestamp', 'action', 'body', )
admin.site.register(models.WPLog, WPLogAdmin)
