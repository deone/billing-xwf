from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import timedelta

from ..models import * 

class PackagesModelsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.subscriber = Subscriber.objects.create(user=self.user,
            country='GHA', phone_number='0542751610')
        self.group = GroupAccount.objects.create(name='CUG',
            max_no_of_users=10)
        self.package = Package.objects.create(package_type='Daily',
            volume='3', speed='1.5')
        now = timezone.now()
        self.gps = GroupPackageSubscription.objects.create(group=self.group,
            package=self.package, start=now,
            stop=now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))
        self.ps = PackageSubscription.objects.create(
            subscriber=self.subscriber, package=self.package, start=now,
            stop=now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))

    def test_package__str__(self):
        string = '%s %s%s' % (self.package.package_type, self.package.volume, 'GB')
        self.assertEqual(self.package.__str__(), string)

    def test_package__str__unlimited_volume(self):
        package = Package.objects.create(package_type='Monthly', volume='Unlimited', speed='1.5')
        string = '%s %s' % (package.package_type, package.volume)
        self.assertEqual(package.__str__(), string)

    def test_gps__str__(self):
        string = '%s %s %s' % (self.group.name, self.package.package_type, self.gps.stop.strftime('%B %d %Y, %I:%M%p'))
        self.assertEqual(self.gps.__str__(), string)

    def test_ps__str__(self):
        string = '%s %s %s' % (self.subscriber.user.email, self.package.package_type, self.gps.stop.strftime('%B %d %Y, %I:%M%p'))
        self.assertEqual(self.ps.__str__(), string)

    def test_gps_is_valid(self):
        self.assertEqual(self.gps.is_valid(), True)
