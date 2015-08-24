from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User
from django import forms

from ..forms import CreateAccountForm, ResetPasswordForm
from ..models import Radcheck
from ..helpers import md5_password

class CreateAccountFormTest(SimpleTestCase):

    def test_clean(self):
        data = {
              'username': 'a@a.com',
              'first_name': 'Ola',
              'last_name': 'Ade',
              'password': '12345',
              'confirm_password': '54321',
              'country': 'NGA',
              'phone_number': '08029299274'
            }

        form = CreateAccountForm(data)

        result = form.is_valid()
        self.assertEqual(result, False)
        self.assertEqual(form.errors['__all__'][0], 'Passwords do not match.')

class ResetPasswordFormTest(TestCase):

    def setUp(self):
        password = '12345'
        self.user = User.objects.create_user('b@b.com', 'b@b.com', password)
        entry = Radcheck.objects.create(
            username=self.user.username, attribute='MD5-Password', op=':=', value=md5_password(password)
        )

    def test_save(self):
        old_password = Radcheck.objects.get(username='b@b.com').value

        data = {'new_password1': '54321', 'new_password2': '54321'}
        form = ResetPasswordForm(self.user, data)
        form.is_valid()
        form.save()

        new_password = Radcheck.objects.get(username='b@b.com').value
        self.assertNotEqual(old_password, new_password)
