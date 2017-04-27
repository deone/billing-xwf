from django.core.urlresolvers import reverse
from django.conf import settings

from . import ViewsTests

class IndexTests(ViewsTests):
    
    def test_index_login_redirect(self):
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, ''.join(
          [reverse(settings.LOGIN_URL), '?next=', reverse('index')]
        ))

    def test_index_with_valid_verified_user(self):
        self.c.post(reverse('accounts:login'), {'username': '0542751610', 'password': '12345'})
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('verified' in response.context)
