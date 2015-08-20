from django.test import TestCase, RequestFactory
from django.test import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

from .helpers import auth_and_login
from .forms import CreateAccountForm, LoginForm

class AccountsViewTests(TestCase):
    def setUp(self):
        # self.factory = RequestFactory()
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
        self.assertTemplateUsed(response, 'accounts/index.html')
        self.assertTrue(isinstance(response.context['form'], CreateAccountForm))

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

    def test_captive_without_get_params(self):
        response = self.client.get(reverse('captive'))
        self.assertEqual(response.status_code, 404)
