from django.test import TestCase
from django.utils import timezone
from django.conf import settings

from datetime import timedelta

from ..admin import GroupPackageSubscriptionAdminForm
from ..models import Package
from accounts.models import GroupAccount

class AdminFormsTest(TestCase):
    
    def setUp(self):
        self.package = Package.objects.create(package_type='Monthly', volume='3', speed='1.5')
        self.ga = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
    
    def test_GroupPackageSubscriptionAdminForm_save(self):
        now = timezone.now()
        form = GroupPackageSubscriptionAdminForm({
            'stop': None,
            'start': now,
            'group': self.ga.pk,
            'package': self.package.pk
        })
        gps = form.save() 
        self.assertEqual((gps.stop - gps.start).days, settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type] / 24)
