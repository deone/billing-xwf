from django.test import SimpleTestCase

from ...forms import PasswordResetSMSForm

class PasswordResetEmailFormTest(SimpleTestCase):

    def setUp(self):
        self.data = {'username': '0554433224'}

    def test_clean(self):
        form = PasswordResetSMSForm(self.data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Phone number does not exist.')
