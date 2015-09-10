from django import forms
from django.contrib import admin

from .models import *

from datetime import timedelta

class GroupPackageSubscriptionAdminForm(forms.ModelForm):

    class Meta:
        model = GroupPackageSubscription
        exclude = ()

    def save(self, commit=True):
        grp_pkg_sub = super(GroupPackageSubscriptionAdminForm, self).save(commit=False)
        package_period = timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[grp_pkg_sub.package.package_type])
        grp_pkg_sub.stop = grp_pkg_sub.start + package_period
        grp_pkg_sub.save()

        return grp_pkg_sub

class GroupPackageSubscriptionAdmin(admin.ModelAdmin):
    form = GroupPackageSubscriptionAdminForm

admin.site.register(Package)
admin.site.register(GroupPackageSubscription, GroupPackageSubscriptionAdmin)
