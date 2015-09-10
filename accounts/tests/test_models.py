from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Subscriber, Radcheck, GroupAccount, AccessPoint
from ..helpers import md5_password

from packages.models import Package

class AccountsModelsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.country = 'NGA'

    def test_subscriber(self):
        country_code = Subscriber.COUNTRY_CODES_MAP[self.country]
        phone_number = country_code + '8029299274'
        subscriber = Subscriber.objects.create(user=self.user, country=self.country, phone_number=phone_number)
        self.assertEqual(subscriber.__str__(), 'a@a.com')

    def test_radcheck(self):
        entry = Radcheck.objects.create(
            username=self.user.username, attribute='MD5-Password', op=':=', value=md5_password('12345')
        )
        self.assertEqual(entry.__str__(), 'a@a.com')

class GroupAccountTests(TestCase):

    def setUp(self):
        self.package = Package.objects.create(package_type='Daily', volume='3', speed='1.5')
        self.group = GroupAccount.objects.create(name='CUG', max_no_of_users=10)

    def test__str__(self):
        self.assertEqual(self.group.__str__(), 'CUG')

class AccessPointTests(TestCase):

    def setUp(self):
        self.package = Package.objects.create(package_type='Daily', volume='3', speed='1.5')
        self.group1 = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        self.group2 = GroupAccount.objects.create(name='LUG', max_no_of_users=10)
        self.ap = AccessPoint.objects.create(name='Djungle HQ 02', mac_address='00:18:0A:F2:DE:20')
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')

        Subscriber.objects.create(user=self.user, country='GHA', phone_number='+233542751610')

    def test__str__(self):
        self.assertEqual(self.ap.__str__(), 'Djungle HQ 02')

    def test_allows_ap_private(self):
        self.assertFalse(self.ap.allows(self.user))

    def test_allows_ap_public(self):
        self.ap.status = 'PUB'
        self.ap.save()
        self.assertTrue(self.ap.allows(self.user))

    def test_allows_ap_subscriber_same_group(self):
        self.ap.group = self.user.subscriber.group = self.group1
        self.ap.save()
        self.user.subscriber.save()
        self.assertTrue(self.ap.allows(self.user))

    def test_allows_ap_subscriber_different_group(self):
        self.ap.group = self.group1
        self.user.subscriber.group = self.group2
        self.ap.save()
        self.user.subscriber.save()
        self.assertFalse(self.ap.allows(self.user))
