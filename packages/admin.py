from django import forms
from django.contrib import admin

from .models import *


class PackageSubscriptionAdminForm(forms.ModelForm):

    class Meta:
        model = PackageSubscription
        exclude = ()

    def save(self, commit=True):
        package_subscription = super(PackageSubscriptionAdminForm, self).save(commit=False)
        package_subscription.stop = compute_stop(package_subscription.start,
            package_subscription.package.package_type)
        package_subscription.save()

        return package_subscription

class GroupPackageSubscriptionAdminForm(forms.ModelForm):

    class Meta:
        model = GroupPackageSubscription
        exclude = ()

    def save(self, commit=True):
        group_package_subscription = super(GroupPackageSubscriptionAdminForm, self).save(commit=False)
        group_package_subscription.stop = compute_stop(group_package_subscription.start,
            group_package_subscription.package.package_type)
        group_package_subscription.save()

        return group_package_subscription

class PackageSubscriptionAdmin(admin.ModelAdmin):
    form = PackageSubscriptionAdminForm

class GroupPackageSubscriptionAdmin(admin.ModelAdmin):
    form = GroupPackageSubscriptionAdminForm

admin.site.register(Package)
admin.site.register(PackageSubscription, PackageSubscriptionAdmin)
admin.site.register(GroupPackageSubscription, GroupPackageSubscriptionAdmin)
