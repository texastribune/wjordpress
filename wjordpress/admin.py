from django.contrib import admin

from . import models


class WPSiteAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'description')
admin.site.register(models.WPSite, WPSiteAdmin)
