from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from ..forms import CreateAccountForm, LoginForm
from ..views import index

class AccountsViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')

    def test_index_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
        self.assertTemplateUsed(response, 'accounts/index.html')
        self.assertTrue(isinstance(response.context['form'], CreateAccountForm))

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
        self.middleware.process_request(request)
        request.session.save()

        # When request.method == 'POST', we use CreateAccountForm and auth_and_login. Test these.
        response = index(request)

        self.assertTrue(response.status_code, 302)

    def test_dashboard_without_authentication(self):
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertRedirects(response, ''.join(
          [reverse(settings.LOGIN_URL), '?next=', reverse('accounts:dashboard')]
        ))

    def test_login_dashboard_redirect(self):
        c = Client()
        response = c.post(reverse('accounts:login'), {'username': 'a@a.com', 'password': '12345'})
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_captive(self):
        get_params = "?login_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Flogin%3Fmauth%3DMMzZUJGqtrsmvkKw6ktCkcNsuBgluav4m2vgE4p-nFliz6lOzP99ntPzZAjvJ_Yit73ZfWwRDIzoEAwzZSuErRpQwdfD0vVA3XjsLLlK8UNiucySNAij7FEqEAF9osnXpWioNcUpyn7BYW8pP5C-wdZAQpLAWS-lv4UTivlfTUn92n4RxMaWG52Q%26continue_url%3Dhttps%253A%252F%252Fn110.network-auth.com%252Fsplash%252Fconnected%253Fhide_terms%253Dtrue&continue_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Fconnected%3Fhide_terms%3Dtrue&ap_mac=00%3A18%3A0a%3Af2%3Ade%3A20&ap_name=Djungle+HQ+02&ap_tags=office-accra+recently-added&client_mac=4c%3A8d%3A79%3Ad7%3A6b%3A28&client_ip=192.168.2.65"
        response = self.client.get(''.join([reverse('captive'), get_params]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')
        self.assertTrue(isinstance(response.context['form'], LoginForm))
        self.assertTrue('login_url' in response.context)
        self.assertTrue('success_url' in response.context)

    def test_captive_without_get_params(self):
        response = self.client.get(reverse('captive'))
        self.assertEqual(response.status_code, 404)

    def test_success(self):
        get_params = "?logout_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Flogout%3Fkey%3DMM7n9oxmBMVzgXgqkvAbLsLTh2cP7lcZdnhrqPRdHlIqzFHCNSRkxoiKzMGmTDQw7dGd092BdPfUs"
        response = self.client.get(''.join([reverse('success'), get_params]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('logout_url' in response.context)

    def test_success_without_get_params(self):
        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
