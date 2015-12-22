from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import timedelta

from ..models import * 
from accounts.helpers import md5_password

class PackagesModelsTests(TestCase):

    def setUp(self):
        username = 'a@a.com'
        password = '12345'
        user = User.objects.create_user(username, username, password)
        self.radcheck = Radcheck.objects.create(user=user,
                                username=username,
                                attribute='MD5-Password',
                                op=':=',
                                value=md5_password(password))
        self.group = GroupAccount.objects.create(name='CUG',
            max_no_of_users=10)
        self.package = Package.objects.create(package_type='Daily',
            volume='3', speed='1.5', price=4)
        now = timezone.now()
        self.gps = GroupPackageSubscription.objects.create(group=self.group,
            package=self.package, start=now,
            stop=now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))
        self.ps = PackageSubscription.objects.create(
            radcheck=self.radcheck, package=self.package, start=now,
            stop=now + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[self.package.package_type]))

    def test_package__str__(self):
        string = '%s %s %s' % (settings.SPEED_NAME_MAP[self.package.speed],
            self.package.package_type, settings.VOLUME_NAME_MAP[self.package.volume])
        self.assertEqual(self.package.__str__(), string)

    def test_gps__str__(self):
        string = '%s %s %s' % (self.group.name, self.package.package_type, self.gps.stop.strftime('%B %d %Y, %I:%M%p'))
        self.assertEqual(self.gps.__str__(), string)

    def test_ps__str__(self):
        string = '%s %s %s' % (self.radcheck.username, self.package.package_type, self.gps.stop.strftime('%B %d %Y, %I:%M%p'))
        self.assertEqual(self.ps.__str__(), string)

    def test_gps_is_valid(self):
        self.assertEqual(self.gps.is_valid(), True)
