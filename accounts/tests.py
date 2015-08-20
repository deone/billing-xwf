from django.test import TestCase, RequestFactory
from django.test import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

from .helpers import auth_and_login
from .forms import CreateAccountForm

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

    def test_captive(TestCase):
        pass
