from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User, AnonymousUser
from django import forms

from ..forms import CreateUserForm, ResetPasswordForm
from ..models import Radcheck, GroupAccount, Subscriber
from ..helpers import md5_password

class CreateUserFormTest(TestCase):

    def setUp(self):
        self.data = {
              'username': 'a@a.com',
              'first_name': 'Ola',
              'last_name': 'Ade',
              'password': '12345',
              'confirm_password': '54321',
              'country': 'NGA',
              'phone_number': '08029299274'
            }

    def test_clean(self):
        form = CreateUserForm(self.data, user=AnonymousUser)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Passwords do not match.')

    def test_save(self):
        user = User.objects.create(username='b@b.com', password='12345')
        ga = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        Subscriber.objects.create(user=user, group=ga, is_group_admin=True, country='GHA', phone_number='+233542751610')

        data = self.data
        data['confirm_password'] = '12345'
        form = CreateUserForm(data, user=user)
        form.is_valid()
        new_user = form.save()

        self.assertEqual(new_user.subscriber.group.name, ga.name)
        self.assertEqual(new_user.subscriber.phone_number, '+2348029299274')

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
