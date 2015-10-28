from django.core.urlresolvers import reverse
from django.conf import settings

from . import ViewsTests

class DashboardTests(ViewsTests):
    
    def test_dashboard_login_redirect(self):
        response = self.c.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, ''.join(
          [reverse(settings.LOGIN_URL), '?next=', reverse('accounts:dashboard')]
        ))

    def test_dashboard_with_valid_verified_user(self):
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('verified' in response.context)
