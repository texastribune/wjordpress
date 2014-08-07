from django.contrib import admin

from . import models


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('wppost', )

admin.site.register(models.Post, PostAdmin)
