from django.contrib import admin

from . import models


class WPSiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.WPSite, WPSiteAdmin)
