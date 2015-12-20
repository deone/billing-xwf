from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from accounts.models import Subscriber
from ..models import Package, PackageSubscription, compute_stop
from ..helpers import check_subscription

from datetime import timedelta

class PackageHelpersTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.subscriber = Subscriber.objects.create(user=user, country='GHA', phone_number='+2348029299274')
        package = Package.objects.create(package_type='Daily', volume='Unlimited', speed='1.5', price=5)
        self.ps = PackageSubscription.objects.create(subscriber=self.subscriber, package=package, start=timezone.now())
        self.ps.stop = compute_stop(self.ps.start, self.ps.package.package_type)
        self.ps.save()

    def test_check_subscription(self):
        self.assertEqual(check_subscription(self.subscriber), self.ps.stop)

    def test_check_invalid_subscription(self):
        self.ps.stop = self.ps.start - timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.ps.package.package_type])
        self.ps.save()

        self.assertEqual(check_subscription(self.subscriber).second, timezone.now().second)
