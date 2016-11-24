from django.core.urlresolvers import reverse

from . import ViewsTests

class PasswordResetCompleteTests(ViewsTests):
    def test_password_reset_complete(self):
        response = self.c.get(reverse('accounts:password_reset_complete'))
        
        self.assertEqual(response.context['login_url'], '/accounts/login/')
        self.assertEqual(response.context['title'], 'Password reset complete')
        self.assertTemplateUsed(response, 'accounts/password_reset_complete.html')