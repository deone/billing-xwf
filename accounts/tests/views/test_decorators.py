from django.core.urlresolvers import reverse

from . import *

"""
We're testing the decorators in billing/decorators.py.
"""

class MustBeGroupAdmin404Test(ViewsTests):

    def test_add_user_get(self):
        self.c.post(reverse('accounts:login'), {'username': '0542751610', 'password': '12345'})
        response = self.c.get(reverse('accounts:add_user'))
        self.assertEqual(response.status_code, 404)

class MustBeIndividualUser404Test(GroupAdminViewsTests):

    def test_recharge_account_get(self):
        self.c.post(reverse('accounts:login'), {'username': '0542751610', 'password': '12345'})
        response = self.c.get(reverse('accounts:recharge_account'))
        self.assertEqual(response.status_code, 404)
