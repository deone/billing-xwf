from django.test import TestCase
from django.core.urlresolvers import reverse

from .forms import CreateAccountForm

class AccountsViewTests(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
        self.assertTemplateUsed(response, 'accounts/index.html')
        self.assertTrue(isinstance(response.context['form'], CreateAccountForm))

    def test_dashboard_view_without_authentication(self):
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertRedirects(response, ''.join(
          [reverse('accounts:login'), '?next=', reverse('accounts:dashboard')]
        ))

    def test_captive(TestCase):
        pass
