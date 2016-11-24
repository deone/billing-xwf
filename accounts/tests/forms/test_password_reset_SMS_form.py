from django.test import TestCase
from django.contrib.auth.models import User

from ...forms import PasswordResetSMSForm

class PasswordResetSMSFormTest(TestCase):

    def setUp(self):
        User.objects.create_user('0231802940', '0231802940', '12345')

    def test_clean(self):
        data = {'username': '0554433224'}
        form = PasswordResetSMSForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Phone number does not exist.')

    def test_save(self):
        data = {'username': '0231802940'}
        form = PasswordResetSMSForm(data)

        self.assertTrue(form.is_valid())
        
        response = form.save()
        self.assertEqual(response.status_code, 201)