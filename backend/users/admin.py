from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['author', 'user']
    search_fields = ['author', 'user']


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscribeAdmin)
