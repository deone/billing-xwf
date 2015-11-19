from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from datetime import timedelta

from ..admin import (
    PackageSubscriptionAdminForm, GroupPackageSubscriptionAdminForm, subscription_package, subscription_group, subscription_subscriber
)
from ..models import *
from accounts.models import GroupAccount, Subscriber

class AdminFormsTest(TestCase):
    
    def setUp(self):
        self.package = Package.objects.create(package_type='Monthly', volume='3', speed='1.5', price=4)
        self.now = timezone.now()
    
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

    def test_PackageSubscriptionAdminForm_save(self):
        user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        subscriber = Subscriber.objects.create(user=user, country='GHA',
            phone_number='0542751610')
        form = PackageSubscriptionAdminForm({
            'stop': None,
            'start': self.now,
            'subscriber': subscriber.pk,
            'package': self.package.pk
        })
        ps = form.save()
        self.assertEqual((ps.stop - ps.start).days,
            settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type] / 24)

    def test_subscription_group(self):
        ga = GroupAccount.objects.create(name='LFG', max_no_of_users=5)
        gps = GroupPackageSubscription.objects.create(group=ga,
            package=self.package, start=self.now,
            stop=self.now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))

        self.assertEqual(subscription_group(gps), 'LFG')

    def test_subscription_subscriber_subscription_package(self):
        user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        subscriber = Subscriber.objects.create(user=user, country='GHA', phone_number='+233542751610')
        ps = PackageSubscription.objects.create(
            subscriber=subscriber, package=self.package, start=self.now,
            stop=self.now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))

        self.assertEqual(subscription_subscriber(ps), 'a@a.com')
        self.assertEqual(subscription_package(ps), '1.5Mbps Deluxe Monthly 3GB')
