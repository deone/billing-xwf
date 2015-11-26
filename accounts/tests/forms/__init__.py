from django.test import TestCase
from django.contrib.auth.models import User

from ...models import (
    GroupAccount, Subscriber
)

class FormsTestCase(TestCase):

    def setUp(self):
        self.group = GroupAccount.objects.create(name='CUG', max_no_of_users=5)
        self.user = User.objects.create_user('e@e.com', 'e@e.com', '12345')
        country = 'GHA'
        self.subscriber = Subscriber.objects.create(user=self.user, group=self.group,
            country=country, phone_number=Subscriber.COUNTRY_CODES_MAP[country] + '555223345')
