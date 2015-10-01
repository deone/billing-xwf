from django import forms
from django.contrib import admin

from .models import *

from datetime import timedelta

def save_subscription(subscription):
    package_period = timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[subscription.package.package_type])
    subscription.stop = subscription.start + package_period
    subscription.save()

class PackageSubscriptionAdminForm(forms.ModelForm):

    class Meta:
        model = PackageSubscription
        exclude = ()

    def save(self, commit=True):
        package_subscription = super(PackageSubscriptionAdminForm, self).save(commit=False)
        save_subscription(package_subscription)

        return package_subscription

class GroupPackageSubscriptionAdminForm(forms.ModelForm):

    class Meta:
        model = GroupPackageSubscription
        exclude = ()

    def save(self, commit=True):
        group_package_subscription = super(GroupPackageSubscriptionAdminForm, self).save(commit=False)
        save_subscription(group_package_subscription)

        return group_package_subscription

class PackageSubscriptionAdmin(admin.ModelAdmin):
    form = PackageSubscriptionAdminForm

class GroupPackageSubscriptionAdmin(admin.ModelAdmin):
    form = GroupPackageSubscriptionAdminForm

admin.site.register(Package)
admin.site.register(PackageSubscription, PackageSubscriptionAdmin)
admin.site.register(GroupPackageSubscription, GroupPackageSubscriptionAdmin)
