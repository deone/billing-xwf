from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.utils import timezone

from ...helpers import (auth_and_login, make_context, md5_password)
from ...forms import (CreateUserForm, LoginForm, BulkUserUploadForm, EditUserForm)
from ...views import (index, resend_mail, add_user, buy_package, upload_user_list, edit_user, toggle_status)
from ...models import (Subscriber, GroupAccount, Radcheck, RechargeAndUsage)

from packages.forms import PackageSubscriptionForm
from packages.models import Package

import os

class AccountsViewsTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.session = SessionMiddleware()
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        country = 'GHA'
        self.subscriber = Subscriber.objects.create(user=self.user,
            country=country, phone_number=Subscriber.COUNTRY_CODES_MAP[country] + '542751610',
            email_verified=True, date_verified=timezone.now())
        self.package = Package.objects.create(package_type='Daily',
            volume='3', speed='1.5', price=4)

    

    

    

    

    

    

    

    def test_upload_user_list_post(self):
        group = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        self.subscriber.group = group
        self.subscriber.save()

        with open(os.path.join(settings.BASE_DIR, 'accounts/tests/views/test_files/test.csv'), 'r') as _file:
            request = self.factory.post(reverse('accounts:upload_user_list'), {'user_list': _file})

        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = upload_user_list(request)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('Users added successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('accounts:upload_user_list'))

    def test_upload_user_list_get(self):
        self.c.post(reverse('accounts:login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('accounts:upload_user_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('file_length' in response.context)
        self.assertEqual(response.context['file_length'], settings.MAX_FILE_LENGTH)
        self.assertTrue(isinstance(response.context['form'], BulkUserUploadForm))
        self.assertTemplateUsed(response, 'accounts/upload_user_list.html')

    def test_edit_user_get(self):
        self.c.post(reverse('accounts:login'), {'username': 'a@a.com', 'password': '12345'})

        user = User.objects.create(email='c@c.com', username='c@c.com', password='12345', is_active=False)
        subscriber = Subscriber.objects.create(user=user,
            country='GHA', email_verified=True, date_verified=timezone.now())

        response = self.c.get(reverse('accounts:edit_user', kwargs={'pk':user.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], EditUserForm))
        self.assertEqual(response.context['form'].initial['phone_number'], "")

    def test_edit_user_post(self):
        user = User.objects.create(email='d@d.com', username='d@d.com', password='12345', is_active=False)
        subscriber = Subscriber.objects.create(user=user,
            country='GHA', phone_number=Subscriber.COUNTRY_CODES_MAP['GHA'] + '542751610',
            email_verified=True, date_verified=timezone.now())
        Radcheck.objects.create(
            user=user, username=user.username, attribute='MD5-Password', op=':=', value=md5_password('12345')
        )

        request = self.factory.post(reverse('accounts:edit_user', kwargs={'pk':user.pk}), data={
              'username': 'b@de.com',
              'first_name': 'Ola',
              'last_name': 'Ade',
              'phone_number': '0542751233'
              })

        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = edit_user(request, pk=user.pk)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        u = User.objects.get(pk=user.pk)
        self.assertEqual(u.email, 'b@de.com')
        self.assertEqual(u.username, 'b@de.com')
        self.assertEqual(u.first_name, 'Ola')
        self.assertEqual(u.last_name, 'Ade')
        self.assertEqual(u.subscriber.phone_number, '+233542751233')
        self.assertEqual(u.radcheck.username, 'b@de.com')

        self.assertEqual(response.status_code, 302)
        self.assertEqual('User changed successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('accounts:view_users'))



