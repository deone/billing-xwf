from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from accounts.tests.views import GroupAdminViewsTests
from accounts.models import Subscriber, GroupAccount

class SearchTests(GroupAdminViewsTests):

    def setUp(self, *args, **kwargs):
        super(SearchTests, self).setUp(*args, **kwargs)
        # Create user we will be searching for
        self.group_member = User.objects.create_user('ola.ade@ooo.com', 'ola.ade@ooo.com', '12345')
        self.group_member.first_name = 'Ola'
        self.group_member.last_name = 'Ade'
        self.group_member.save()

        Subscriber.objects.create(user=self.group_member, country='NGA', phone_number='+233542751610', group=self.group)

    def test_index(self):
        self.c.post(reverse('accounts:login'), {'username': '0542751610', 'password': '12345'})
        response = self.c.get(reverse('search:index'), {'q': 'ooo ade'})
        user = response.context['users'][0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.first_name, self.group_member.first_name)
        self.assertEqual(user.last_name, self.group_member.last_name)
        self.assertEqual(user.username, self.group_member.username)
