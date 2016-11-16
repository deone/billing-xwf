from django.test import TestCase, RequestFactory, Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, AnonymousUser
from django.utils import timezone

from ...models import Subscriber, GroupAccount, Radcheck
from ...helpers import md5_password

class ViewsTests(TestCase):
    
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.session = SessionMiddleware()
        username = '0542751610'
        password = '12345'
        self.user = User.objects.create_user(username, username, password)
        country = 'GHA'
        self.subscriber = Subscriber.objects.create(user=self.user,
            country=country, phone_number=Subscriber.COUNTRY_CODES_MAP[country] + '542751610',
            email_verified=True, date_verified=timezone.now())
        self.radcheck = Radcheck.objects.create(user=self.user,
                                username=username,
                                attribute='MD5-Password',
                                op=':=',
                                value=md5_password(password))
        self.group = GroupAccount.objects.create(name='CUG', max_no_of_users=2)

class GroupAdminViewsTests(ViewsTests):

    def setUp(self, *args, **kwargs):
        super(GroupAdminViewsTests, self).setUp(*args, **kwargs)
        self.subscriber.group = self.group
        self.subscriber.is_group_admin = True
        self.subscriber.save()
