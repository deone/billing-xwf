from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from datetime import timedelta

from ..admin import PackageSubscriptionAdminForm, GroupPackageSubscriptionAdminForm
from ..models import Package
from accounts.models import GroupAccount, Subscriber

class AdminFormsTest(TestCase):
    
    def setUp(self):
        self.package = Package.objects.create(package_type='Monthly', volume='3', speed='1.5')
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
