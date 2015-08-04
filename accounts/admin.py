from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class SubscriberInline(admin.StackedInline):
    model = Subscriber
    can_delete = False
    verbose_name_plural = 'subscribers'

@admin.register(Radcheck)
class RadcheckAdmin(admin.ModelAdmin):
    pass

class UserAdmin(UserAdmin):
    inlines = (SubscriberInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
