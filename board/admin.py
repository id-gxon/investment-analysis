from django.contrib import admin
from .models import Discussion


class DiscussionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Discussion, DiscussionAdmin)
