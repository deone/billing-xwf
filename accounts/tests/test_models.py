from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Subscriber, Radcheck
from ..helpers import md5_password

class AccountsModelsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.country = 'NGA'

    def test_subscriber(self):
        country_code = Subscriber.COUNTRY_CODES_MAP[self.country]
        phone_number = country_code + '8029299274'
        subscriber = Subscriber.objects.create(user=self.user, country=self.country, phone_number=phone_number)
        self.assertEquals(subscriber.__str__(), 'a@a.com')

    def test_radcheck(self):
        entry = Radcheck.objects.create(
            username=self.user.username, attribute='MD5-Password', op=':=', value=md5_password('12345')
        )
        self.assertEquals(entry.__str__(), 'a@a.com')
