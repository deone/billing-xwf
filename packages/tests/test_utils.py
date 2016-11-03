from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from accounts.models import Radcheck 
from accounts.helpers import md5_password
from ..models import Package, PackageSubscription

from utils import compute_stop_time, check_subscription

from datetime import timedelta

class PackageUtilsTest(TestCase):

    def setUp(self):
        username = '0542751610'
        password = '12345'
        user = User.objects.create_user(username, username, password)
        self.radcheck = Radcheck.objects.create(user=user,
                                username=username,
                                attribute='MD5-Password',
                                op=':=',
                                value=md5_password(password),
                                data_balance=1)
        package = Package.objects.create(package_type='Daily', volume='Unlimited', speed='1.5', price=5)
        
        """
        Note about microsecond precision
        ================================
        test_check_subscription fails when we use self.ps as returned by create.
        This ps object contains the microseconds value which 
        self.radcheck.packagesubscription_set.all()[0] does not return.
        To fix this, we are just going to create the object and select it 
        from the database to get rid of the microseconds value.
        """
        PackageSubscription.objects.create(radcheck=self.radcheck, package=package, start=timezone.now())
        self.ps = PackageSubscription.objects.get(radcheck=self.radcheck)
        self.ps.stop = compute_stop_time(self.ps.start, self.ps.package.package_type)
        self.ps.save()

    def test_check_subscription(self):
        self.assertEqual(check_subscription(self.radcheck), self.ps.stop)

    def test_check_invalid_subscription(self):
        self.ps.stop = self.ps.start - timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.ps.package.package_type])
        self.ps.save()

        self.assertEqual(check_subscription(self.radcheck).second, timezone.now().second)
