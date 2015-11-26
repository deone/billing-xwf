from django.test import TestCase, RequestFactory, Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, AnonymousUser
from django.utils import timezone

from ...models import Subscriber, GroupAccount

class ViewsTests(TestCase):
    
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.session = SessionMiddleware()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')
        country = 'GHA'
        self.subscriber = Subscriber.objects.create(user=self.user,
            country=country, phone_number=Subscriber.COUNTRY_CODES_MAP[country] + '555223345',
            email_verified=True, date_verified=timezone.now())
        self.group = GroupAccount.objects.create(name='CUG', max_no_of_users=2)
