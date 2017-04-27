from django.test import TestCase
from django.contrib.auth.models import User

from ...models import (
    GroupAccount, Subscriber
)

class FormsTestCase(TestCase):

    def setUp(self):
        phone_number = '0555223345'
        self.group = GroupAccount.objects.create(name='CUG', max_no_of_users=5)
        self.user = User.objects.create_user(phone_number, phone_number, '12345')
        country = 'GHA'
        self.subscriber = Subscriber.objects.create(user=self.user, group=self.group,
            country=country, phone_number=Subscriber.COUNTRY_CODES_MAP[country] + phone_number[1:])
