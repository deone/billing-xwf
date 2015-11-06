from django import forms
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from ..models import GroupAccount, Subscriber, AccessPoint
from ..admin import (
    AccountsUserCreationForm, AccountsUserChangeForm, AccessPointAdminForm, SubscriberAdminForm, user_group, ap_group
)

class AdminFormsTest(TestCase):

    def setUp(self):
        self.help_text = "Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."
    
    def test_AccountsUserCreationForm(self):
        a = AccountsUserCreationForm()
        self.assertEqual(a.fields['username'].help_text, self.help_text)

    def test_AccountsUserCreationForm_save(self):
        form = AccountsUserCreationForm({'username': 'a@a.com', 'password1': '12345', 'password2': '12345'})
        user = form.save()
        self.assertEqual(user.email, 'a@a.com')
        self.assertEqual(user.radcheck.__str__(), 'a@a.com')

    def test_AccountsUserChangeForm(self):
        a = AccountsUserChangeForm()
        self.assertEqual(a.fields['username'].help_text, self.help_text)

class GroupAccountRelatedTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='b@b.com', password='12345')
        self.ga = GroupAccount.objects.create(name='CUG', max_no_of_users=10)

    def test_AccessPointAdminForm_invalid(self):
        form = AccessPointAdminForm({'name': 'HQ', 'group': self.ga.pk, 'mac_address': '00:18:0A:F2:DE:20', 'status': 'PUB'})
        self.assertFalse(form.is_valid())
        # print form.is_valid()
        # with self.assertRaises(forms.ValidationError):
            # form.clean()

    def test_AccessPointAdminForm_valid(self):
        form = AccessPointAdminForm({'name': 'HQ', 'group': self.ga.pk, 'mac_address': '00:18:0A:F2:DE:20', 'status': 'PRV'})
        self.assertTrue(form.is_valid())
        # print form.clean()

    def test_SubscriberAdminForm_invalid(self):
        form = SubscriberAdminForm({
          'phone_number': '0542751610',
          'group': self.ga.pk,
          'is_group_admin': False,
          'country': 'GHA',
          'date_verified': None,
          'user': self.user.pk,
          'email_verified': False,
          'id': None})
        self.assertFalse(form.is_valid())

    def test_SubscriberAdminForm_save(self):
        form = SubscriberAdminForm({
          'phone_number': '0542751610',
          'group': self.ga.pk,
          'is_group_admin': True,
          'country': 'GHA',
          'date_verified': None,
          'user': self.user.pk,
          'email_verified': False,
          'id': None})
        self.assertTrue(form.is_valid())
        subscriber = form.save()
        self.assertEqual(subscriber.phone_number, '+233542751610')

    def test_user_group(self):
        Subscriber.objects.create(user=self.user, group=self.ga, is_group_admin=True,
            country='GHA', phone_number='+233542751610')
        group_name = user_group(self.user)
        self.assertEqual(group_name, 'CUG')

    def test_ap_group(self):
        ap = AccessPoint.objects.create(name='Djungle HQ 02', group=self.ga, mac_address='00:18:0A:F2:DE:20')
        group_name = ap_group(ap)
        self.assertEqual(group_name, 'CUG')
