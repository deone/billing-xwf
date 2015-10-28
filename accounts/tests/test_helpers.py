from django.core.urlresolvers import reverse

from ..helpers import auth_and_login

from views import ViewsTests

class HelpersTests(ViewsTests):

    def test_auth_and_login_fail(self):
        request = self.factory.get(reverse('accounts:login'))
        response = auth_and_login(request, 'b@b.com', '1234')
        self.assertEqual(response, False)
