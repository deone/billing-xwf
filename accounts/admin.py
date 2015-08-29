from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class SubscriberInline(admin.StackedInline):
    model = Subscriber
    can_delete = False
    verbose_name_plural = 'subscribers'

class UserAdmin(UserAdmin):
    inlines = (SubscriberInline, )

admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
