from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from accounts.tests.views import GroupAdminViewsTests

class SearchTests(GroupAdminViewsTests):

    def setUp(self, *args, **kwargs):
        super(SearchTests, self).setUp(*args, **kwargs)
        # Create user we will be searching for
        self.user = User.objects.create_user('ola.ade@ooo.com', 'ola.ade@ooo.com', '12345')
        self.user.first_name = 'Ola'
        self.user.last_name = 'Ade'
        self.user.save()

    def test_index(self):
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('search:index'), {'q': 'ooo ade'})
        user = response.context['users'][0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.first_name, self.user.first_name)
        self.assertEqual(user.last_name, self.user.last_name)
        self.assertEqual(user.username, self.user.username)
