from django.test import TestCase, RequestFactory, Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, AnonymousUser
from django.utils import timezone

from ...models import Subscriber, GroupAccount, Radcheck, NetworkParameter
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
        NetworkParameter.objects.create(
                    subscriber=self.subscriber,
                    login_url='https://n110.network-auth.com/splash/login?mauth=MMNsInqn8ksWBR7PgbfBkWG8PawzJm1wi4PE9pDEUdU1qFuHtYczZmRJFJ3dD7AJvl9DRppZnJAZOTA7L3KbzaX4WgwU74t5ibpIJBwHJ-eg5RnL4Hct5hs7i1UIRBH6kbeL9X4hlcFLZKvkaV2mpeP_hX9hxs5jGl_C0N6oWtoQtUjskrMcnBaA&continue_url=http%3A%2F%2Fgoogle.com%2F',
                    continue_url='http://google.com/',
                    ap_mac='00:18:0a:f2:de:20',
                    ap_name='Spectra-HQ-NOC',
                    ap_tags='office-accra recently-added',
                    client_mac='4c:eb:42:ce:6c:3d',
                    client_ip='10.8.0.78',
                    )
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
