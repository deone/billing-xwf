from django.test import TestCase
from django.utils import timezone

from datetime import timedelta

from ..models import * 

class PackagesModelsTests(TestCase):

    def setUp(self):
        self.group = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        self.package = Package.objects.create(package_type='Daily', volume='3', speed='1.5')
        now = timezone.now()
        self.gps = GroupPackageSubscription.objects.create(group=self.group, package=self.package, start=now,
            stop=now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))

    def test_package__str__(self):
        self.assertEqual(self.package.__str__(), 'Daily 3GB')

    def test_gps__str__(self):
        self.assertEqual(self.gps.__str__(), 'CUG Daily ' + self.gps.stop.strftime('%B %d %Y, %I:%M%p'))
