from django.contrib import admin

from . import models


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_filter = ('pub_status', )
    readonly_fields = ('wppost', )

admin.site.register(models.Post, PostAdmin)
