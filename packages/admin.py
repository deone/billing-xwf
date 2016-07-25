from django import forms
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .forms import update_cleaned_data
from .models import *

from accounts.models import GroupAccount

from utils import *

from decimal import Decimal

class PackageSubscriptionAdminForm(forms.ModelForm):

    class Meta:
        model = PackageSubscription
        exclude = ()

    def clean(self):
        cleaned_data = super(PackageSubscriptionAdminForm, self).clean()
        radcheck = cleaned_data.get('radcheck')
        package = cleaned_data.get('package')

        start, amount, balance = check_balance_and_subscription(radcheck, package)
        update_cleaned_data(cleaned_data, {'start': start, 'amount': amount, 'balance': balance})

    def save(self, commit=True):
        radcheck = self.cleaned_data['radcheck']
        amount = self.cleaned_data['amount']
        balance = self.cleaned_data['balance']
        package = self.cleaned_data['package']

        # Charge subscriber for package
        charge_subscriber(radcheck, amount, balance, package)

        # Increment data balance
        if package.volume != 'Unlimited':
            increment_data_balance(radcheck, package)

        package_subscription = super(PackageSubscriptionAdminForm, self).save(commit=False)
        package_subscription.stop = compute_stop_time(package_subscription.start,
            package_subscription.package.package_type)
        package_subscription.save()

        return package_subscription

class GroupPackageSubscriptionAdminForm(forms.ModelForm):

    class Meta:
        model = GroupPackageSubscription
        exclude = ()

    def clean(self):
        cleaned_data = super(GroupPackageSubscriptionAdminForm, self).clean()
        group = cleaned_data.get('group')
        start = check_subscription(group=group)
        cleaned_data['start'] = start

    def save(self, commit=True):
        group_package_subscription = super(GroupPackageSubscriptionAdminForm, self).save(commit=False)
        group_package_subscription.stop = compute_stop_time(group_package_subscription.start,
            group_package_subscription.package.package_type)
        group_package_subscription.save()

        group = GroupAccount.objects.get(pk=group_package_subscription.group.pk)
        if group_package_subscription.package.volume != 'Unlimited':
            group.data_balance += Decimal(group_package_subscription.package.volume)
        group.save()

        return group_package_subscription

def subscription_package(obj):
    return obj.package.__str__()

subscription_package.short_description = 'Package'
subscription_package.admin_order_field = 'package__package_type'

def subscription_group(obj):
    return obj.group.name

subscription_group.short_description = 'Group'
subscription_group.admin_order_field = 'group__name'

def subscription_radcheck(obj):
    return obj.radcheck.username

subscription_radcheck.short_description = 'Subscriber'
subscription_radcheck.admin_order_field = 'radcheck__username'

class StopBooleanListFilter(admin.SimpleListFilter):

    title = _('expired?')
    parameter_name = 'is_expired'

    def lookups(self, request, model_admin):
        return (
                  ('0', _('No')),
                  ('1', _('Yes')),
              )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(stop__lt=timezone.now())

        if self.value() == '0':
            return queryset.filter(stop__gt=timezone.now())

class PackageSubscriptionAdmin(admin.ModelAdmin):
    form = PackageSubscriptionAdminForm
    list_display = (subscription_package, 'start', 'stop', subscription_radcheck)
    list_filter = (StopBooleanListFilter,)
    search_fields = ('package__package_type', 'radcheck__username')

class GroupPackageSubscriptionAdmin(admin.ModelAdmin):
    form = GroupPackageSubscriptionAdminForm
    list_display = (subscription_package, 'start', 'stop', subscription_group)
    list_filter = (StopBooleanListFilter,)
    search_fields = ('package__package_type', 'group__name')

class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_type', 'volume', 'speed', 'price', 'is_public')
    search_fields = ('package_type', 'volume', 'speed')

admin.site.register(Package, PackageAdmin)
admin.site.register(PackageSubscription, PackageSubscriptionAdmin)
admin.site.register(GroupPackageSubscription, GroupPackageSubscriptionAdmin)
