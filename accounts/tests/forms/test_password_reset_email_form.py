from django.test import SimpleTestCase

from ...forms import PasswordResetEmailForm

class PasswordResetEmailFormTest(SimpleTestCase):

    def setUp(self):
        self.data = {'email': 'z@z.com'}

    def test_clean(self):
        form = PasswordResetEmailForm(self.data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Email does not exist.')
