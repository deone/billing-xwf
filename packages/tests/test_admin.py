from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin

from datetime import timedelta

from ..admin import (
    PackageSubscriptionAdminForm, GroupPackageSubscriptionAdminForm, subscription_package, subscription_group, subscription_radcheck
)
from ..models import *
from accounts.models import (GroupAccount, Subscriber, RechargeAndUsage)
from accounts.helpers import md5_password

class MockRequest(object):
    pass

class AdminTests(TestCase):

    def setUp(self):
        self.package = Package.objects.create(package_type='Monthly', volume='3', speed='1.5', price=4)
        self.now = timezone.now()
        self.site = AdminSite()
        self.request = MockRequest()

class PackageSubscriptionAdminTests(AdminTests):

    def setUp(self, *args, **kwargs):
        super(PackageSubscriptionAdminTests, self).setUp(*args, **kwargs)
        username = 'a@a.com'
        password = '12345'
        user = User.objects.create_user(username, username, password)
        self.radcheck = Radcheck.objects.create(user=user,
                                username=username,
                                attribute='MD5-Password',
                                op=':=',
                                value=md5_password(password))

    def test_get_queryset(self):
        ps = PackageSubscription.objects.create(
            radcheck=self.radcheck, package=self.package, start=self.now,
            stop=self.now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))

        ma = ModelAdmin(PackageSubscription, self.site)
        qs = ma.get_queryset(self.request)

        self.assertTrue(qs[0].stop > self.now)
    
    def test_subscription_radcheck_subscription_package(self):
        ps = PackageSubscription.objects.create(
            radcheck=self.radcheck, package=self.package, start=self.now,
            stop=self.now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))

        self.assertEqual(subscription_radcheck(ps), 'a@a.com')
        self.assertEqual(subscription_package(ps), '1.5Mbps Deluxe Monthly')

    def test_PackageSubscriptionAdminForm_save(self):
        RechargeAndUsage.objects.create(
            radcheck=self.radcheck,
            amount=20,
            balance=20,
            action='REC',
            activity_id=5
        )
        form = PackageSubscriptionAdminForm({
            'stop': None,
            'start': self.now,
            'radcheck': self.radcheck.pk,
            'package': self.package.pk
        })
        form.is_valid()
        ps = form.save()
        self.assertEqual((ps.stop - ps.start).days,
            settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type] / 24)

class GroupPackageSubscriptionAdminTests(AdminTests):
    
    def test_GroupPackageSubscriptionAdminForm_save(self):
        ga = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        form = GroupPackageSubscriptionAdminForm({
            'stop': None,
            'start': self.now,
            'group': ga.pk,
            'package': self.package.pk
        })
        gps = form.save()
        self.assertEqual((gps.stop - gps.start).days,
            settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type] / 24) 

    def test_subscription_group(self):
        ga = GroupAccount.objects.create(name='LFG', max_no_of_users=5)
        gps = GroupPackageSubscription.objects.create(group=ga,
            package=self.package, start=self.now,
            stop=self.now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))

        self.assertEqual(subscription_group(gps), 'LFG') 

    def test_gps_get_queryset(self):
        ga = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        gps = GroupPackageSubscription.objects.create(group=ga,
            package=self.package, start=self.now,
            stop=self.now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))

        ma = ModelAdmin(GroupPackageSubscription, self.site)
        qs = ma.get_queryset(self.request)

        self.assertTrue(qs[0].stop > self.now)
