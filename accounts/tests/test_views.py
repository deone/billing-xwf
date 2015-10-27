from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.utils import timezone

from ..helpers import auth_and_login, make_context, md5_password
from ..forms import CreateUserForm, LoginForm, BulkUserUploadForm, EditUserForm
from ..views import index, resend_mail, add_user, buy_package, upload_user_list, edit_user, toggle_active
from ..models import Subscriber, GroupAccount, Radcheck

from packages.forms import PackageSubscriptionForm
from packages.models import Package

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

    def test_index_get(self):
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
        self.assertTemplateUsed(response, 'accounts/index.html')
        self.assertTrue(isinstance(response.context['form'], CreateUserForm))

    def test_index_post(self):
        request = self.factory.post(reverse('index'),
            data={
              'username': 'b@b.com',
              'password': '12345',
              'first_name': 'Ola',
              'last_name': 'Ade',
              'confirm_password': '12345',
              'country': 'GHA',
              'phone_number': '0542751610'
              })
        request.user = AnonymousUser
        self.session.process_request(request)
        request.session.save()

        response = index(request)

        self.assertTrue(response.status_code, 302)
        self.assertEqual(response.get('location'), reverse('accounts:dashboard'))

    def test_dashboard_login_redirect(self):
        response = self.c.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, ''.join(
          [reverse(settings.LOGIN_URL), '?next=', reverse('accounts:dashboard')]
        ))

    def test_dashboard_with_valid_verified_user(self):
        self.c.post(reverse('accounts:login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('verified' in response.context)

    def test_login(self):
        response = self.c.post(reverse('accounts:login'), {'username': 'a@a.com', 'password': '12345'})
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_login_fail(self):
        response = self.c.post(reverse('accounts:login'), {'username': 'b@b.com', 'password': '12345'})
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_auth_and_login_fail(self):
        request = self.factory.get(reverse('accounts:login'))
        response = auth_and_login(request, 'b@b.com', '1234')
        self.assertEqual(response, False)

    def test_captive(self):
        get_params = "?login_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Flogin%3Fmauth%3DMMzZUJGqtrsmvkKw6ktCkcNsuBgluav4m2vgE4p-nFliz6lOzP99ntPzZAjvJ_Yit73ZfWwRDIzoEAwzZSuErRpQwdfD0vVA3XjsLLlK8UNiucySNAij7FEqEAF9osnXpWioNcUpyn7BYW8pP5C-wdZAQpLAWS-lv4UTivlfTUn92n4RxMaWG52Q%26continue_url%3Dhttps%253A%252F%252Fn110.network-auth.com%252Fsplash%252Fconnected%253Fhide_terms%253Dtrue&continue_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Fconnected%3Fhide_terms%3Dtrue&ap_mac=00%3A18%3A0a%3Af2%3Ade%3A20&ap_name=Djungle+HQ+02&ap_tags=office-accra+recently-added&client_mac=4c%3A8d%3A79%3Ad7%3A6b%3A28&client_ip=192.168.2.65"
        response = self.c.get(''.join([reverse('captive'), get_params]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')
        self.assertTrue(isinstance(response.context['form'], LoginForm))
        self.assertTrue('login_url' in response.context)
        self.assertTrue('success_url' in response.context)

    def test_captive_with_error_message(self):
        get_params = "?login_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Flogin%3Fmauth%3DMMzZUJGqtrsmvkKw6ktCkcNsuBgluav4m2vgE4p-nFliz6lOzP99ntPzZAjvJ_Yit73ZfWwRDIzoEAwzZSuErRpQwdfD0vVA3XjsLLlK8UNiucySNAij7FEqEAF9osnXpWioNcUpyn7BYW8pP5C-wdZAQpLAWS-lv4UTivlfTUn92n4RxMaWG52Q%26continue_url%3Dhttps%253A%252F%252Fn110.network-auth.com%252Fsplash%252Fconnected%253Fhide_terms%253Dtrue&error_message=Access+denied+for+herbertellisspectradjungle%40spectrawireless.com&continue_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Fconnected%3Fhide_terms%3Dtrue&ap_mac=00%3A18%3A0a%3Af2%3Ade%3A20&ap_name=Djungle+HQ+02&ap_tags=office-accra+recently-added&client_mac=4c%3A8d%3A79%3Ad7%3A6b%3A28&client_ip=192.168.2.65"
        response = self.c.get(''.join([reverse('captive'), get_params]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('error_message' in response.context)

    def test_captive_without_get_params(self):
        response = self.c.get(reverse('captive'))
        self.assertEqual(response.status_code, 404)

    def test_success(self):
        get_params = "?logout_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Flogout%3Fkey%3DMM7n9oxmBMVzgXgqkvAbLsLTh2cP7lcZdnhrqPRdHlIqzFHCNSRkxoiKzMGmTDQw7dGd092BdPfUs"
        response = self.c.get(''.join([reverse('success'), get_params]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('logout_url' in response.context)

    def test_success_without_get_params(self):
        response = self.c.get(reverse('success'))
        self.assertEqual(response.status_code, 200)

    def test_verify_email(self):
        self.subscriber.email_verified = False
        self.subscriber.date_verified = None
        self.subscriber.save()

        request = self.factory.get(reverse('index'))
        context = make_context(self.user)

        response = self.c.get(reverse('accounts:verify_email',
          kwargs={'uidb64':context['uid'], 'token': context['token']}))

        subscriber = Subscriber.objects.get(pk=self.subscriber.pk)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:dashboard'),
            status_code=302, target_status_code=302)
        self.assertEqual(subscriber.email_verified, True)
        self.assertNotEqual(subscriber.date_verified, None)

    def test_verify_email_404(self):
        response = self.c.get(reverse('accounts:verify_email',
          kwargs={'uidb64':'Ng', 'token': '44l-013ea9fff05d175d1ccb'}))
        self.assertEqual(response.status_code, 404)

    def test_resend_mail(self):
        request = self.factory.get(reverse('index'))
        request.user = self.user
        response = resend_mail(request)
        self.assertEqual(response.status_code, 302)

    def test_add_user_get(self):
        self.c.post(reverse('accounts:login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('accounts:add_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], CreateUserForm))
        self.assertTemplateUsed(response, 'accounts/add_user.html')

    def test_add_user_post(self):
        request = self.factory.post(reverse('accounts:add_user'),
            data={
              'username': 'b@b.com',
              'password': '12345',
              'first_name': 'Ola',
              'last_name': 'Ade',
              'confirm_password': '12345',
              'country': 'GHA',
              'phone_number': '0542751610'
              })
        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = add_user(request)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('User added successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('accounts:add_user'))

    def test_buy_package_get(self):
        self.c.post(reverse('accounts:login'), {'username': 'a@a.com', 'password': '12345'})
        response = self.c.get(reverse('accounts:buy_package'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'accounts/buy_package.html')

    def test_buy_package_post(self):
        request = self.factory.post(reverse('accounts:buy_package'),
            data={
              'package_choice': str(self.package.pk)
              })
        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = buy_package(request)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), reverse('accounts:buy_package'))
        self.assertEqual('Package purchased successfully.', lst[0].__str__())

    def test_upload_user_list_post(self):
        group = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        self.subscriber.group = group
        self.subscriber.save()

        with open('/Users/deone/src/billing/billing/accounts/tests/test_files/test.csv') as _file:
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

class ViewsTests(TestCase):
    
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.session = SessionMiddleware()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')
        country = 'GHA'
        self.subscriber = Subscriber.objects.create(user=self.user,
            country=country, phone_number=Subscriber.COUNTRY_CODES_MAP[country] + '555223345')
        self.group = GroupAccount.objects.create(name='CUG', max_no_of_users=2)
        self.factory = RequestFactory()
        

class ToggleUserStatusTests(ViewsTests):

    def create_user(self, is_active=True):
        user = User.objects.create_user('b@b.com', 'b@b.com', '12345')
        user.is_active = is_active
        user.save()

        return user

    def create_group_user(self, email):
        country = 'GHA'
        if not self.group.max_user_count_reached():
            user = User.objects.create_user(email, email, '12345')
            user.subscriber = Subscriber.objects.create(user=user, group=self.group,
                country=country, phone_number=Subscriber.COUNTRY_CODES_MAP[country] + '555223345')
            user.subscriber.save()

        return user

    def get_user(self, pk):
        return User.objects.get(pk=pk)

    def send_request(self, pk):
        return self.c.get(reverse('accounts:toggle_active', kwargs={'pk':pk}))

    def check_response(self, response):
        self.assertRedirects(response, reverse('accounts:view_users'))
        self.assertEqual(response.status_code, 302)

    def set_group_group_admin(self):
        """ Set group and group_admin status for user. """
        self.user.subscriber.group = self.group
        self.user.subscriber.is_group_admin = True
        self.user.subscriber.save()

    def test_toggle_status_inactive(self):
        """ Test that user.is_active is set to False. """

        # Set group and group_admin status for user sending this request.
        # Only group_admins are allowed to perform this action. We might need to write a
        # custom decorator to ensure this so that a random logged-in user doesn't just
        # enter the URL and performs this action.
        self.set_group_group_admin()

        # Log user in, since login is required
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})

        # Create user. We don't need to bother with creating subscriber and group instances
        # for this user since those are not checked when we're deactivating user.
        user = self.create_user()

        # Send request and get response
        response = self.send_request(user.pk)

        # Fetch user instance and perform checks.
        deactivated_user = self.get_user(user.pk)

        self.assertFalse(deactivated_user.is_active)
        self.check_response(response)

    def test_toggle_status_active(self):
        """ Test that user.is_active is set to True. """

        self.set_group_group_admin()

        # Log user in
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})

        # Create user
        user = self.create_user(is_active=False)

        # Send request and get response
        response = self.send_request(user.pk)

        # Fetch user instance and perform checks
        activated_user = self.get_user(user.pk)

        self.assertTrue(activated_user.is_active)
        self.check_response(response)

    def test_toggle_status_active_max_user_count_reached(self):
        """ Test that group admin is unable to set user.is_active to True if group has reached its max. no of users. """

        self.set_group_group_admin()

        # Log user in, since login is required
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})

        # Create second user. Group admin is the first
        second_user = self.create_group_user('p@p.com')

        # Deactivate second_user to free slot to create another
        second_user.is_active = False
        second_user.save()

        # Create third user.
        third_user = self.create_group_user('s@s.com')

        # Attempt making second_user active.
        request = self.factory.post(reverse('accounts:toggle_active', kwargs={'pk':second_user.pk}))

        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = toggle_active(request, pk=second_user.pk)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        # Fetch user again so that we can check it
        inactive_user = self.get_user(second_user.pk)

        # Check that user wasn't made active
        # Also check that error message was added to message storage
        self.assertFalse(inactive_user.is_active)
        self.assertTrue(lst[0].__str__().startswith("You are not allowed"))
