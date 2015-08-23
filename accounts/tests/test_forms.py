from django.test import SimpleTestCase
from django import forms

from ..forms import CreateAccountForm, ResetPasswordForm

class AccountsFormsTests(SimpleTestCase):

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

    def test_save(self):
        pass
