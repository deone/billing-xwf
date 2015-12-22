from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from accounts.models import Radcheck 
from accounts.helpers import md5_password
from ..models import Package, PackageSubscription, compute_stop
from ..helpers import check_subscription

from datetime import timedelta

class PackageHelpersTest(TestCase):

    def setUp(self):
        username = 'a@a.com'
        password = '12345'
        user = User.objects.create_user(username, username, password)
        self.radcheck = Radcheck.objects.create(user=user,
                                username=username,
                                attribute='MD5-Password',
                                op=':=',
                                value=md5_password(password))
        package = Package.objects.create(package_type='Daily', volume='Unlimited', speed='1.5', price=5)
        self.ps = PackageSubscription.objects.create(radcheck=self.radcheck, package=package, start=timezone.now())
        self.ps.stop = compute_stop(self.ps.start, self.ps.package.package_type)
        self.ps.save()

    def test_check_subscription(self):
        self.assertEqual(check_subscription(self.radcheck), self.ps.stop)

    def test_check_invalid_subscription(self):
        self.ps.stop = self.ps.start - timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.ps.package.package_type])
        self.ps.save()

        self.assertEqual(check_subscription(self.radcheck).second, timezone.now().second)
