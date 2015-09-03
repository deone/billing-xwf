from django import forms
from django.test import TestCase

from ..models import GroupAccount
from ..admin import AccountsUserCreationForm, AccountsUserChangeForm, AccessPointAdminForm

class AdminFormsTest(TestCase):

    def setUp(self):
        self.help_text = "Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."
        self.ga = GroupAccount.objects.create(name='CUG', max_user_quantity=10)
    
    def test_accounts_user_creation_form(self):
        a = AccountsUserCreationForm()
        self.assertEqual(a.fields['username'].help_text, self.help_text)

    def test_accounts_user_change_form(self):
        a = AccountsUserChangeForm()
        self.assertEqual(a.fields['username'].help_text, self.help_text)

    def test_access_point_admin_form_invalid(self):
        form = AccessPointAdminForm({'name': 'HQ', 'group': self.ga.pk, 'mac_address': '00:18:0A:F2:DE:20', 'status': 'PUB'})
        self.assertFalse(form.is_valid())
        # print form.is_valid()
        # with self.assertRaises(forms.ValidationError):
            # form.clean()

    def test_access_point_admin_form_valid(self):
        form = AccessPointAdminForm({'name': 'HQ', 'group': self.ga.pk, 'mac_address': '00:18:0A:F2:DE:20', 'status': 'PRV'})
        self.assertTrue(form.is_valid())
        # print form.clean()
