from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django import forms

from ..forms import CreateUserForm, ResetPasswordForm, PasswordResetEmailForm, BulkUserUploadForm
from ..models import Radcheck, GroupAccount, Subscriber
from ..helpers import md5_password

import os

class CreateUserFormTest(TestCase):

    def setUp(self):
        self.group = GroupAccount.objects.create(name='CUG', max_no_of_users=1)
        self.user = User.objects.create_user('e@e.com', 'e@e.com', '12345')
        country = 'GHA'
        self.subscriber = Subscriber.objects.create(user=self.user, group=self.group,
            country=country, phone_number=Subscriber.COUNTRY_CODES_MAP[country] + '555223345')
        self.data = {
              'username': 'a@a.com',
              'first_name': 'Ola',
              'last_name': 'Ade',
              'password': '12345',
              'confirm_password': '54321',
              'country': 'NGA',
              'phone_number': '08029299274'
            }

    def test_clean_password_mismatch(self):
        form = CreateUserForm(self.data, user=AnonymousUser)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Passwords do not match.')

    def test_clean_max_user_count_reached(self):
        data = self.data
        data['confirm_password'] = '12345'
        form = CreateUserForm(data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['__all__'][0].startswith(
          'You are not allowed to create more users than your group threshold.'
          ))

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

class PasswordResetEmailFormTest(TestCase):

    def setUp(self):
        self.data = {'email': 'z@z.com'}

    def test_clean(self):
        form = PasswordResetEmailForm(self.data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Email does not exist.')

class BulkUserUploadFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='u@u.com', password='12345')
        group = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        subscriber = Subscriber.objects.create(user=self.user, country='GHA', phone_number='0542751610', group=group)

        path = os.path.join(settings.BASE_DIR, 'accounts/tests/views/test_files/')
        self.txt_file = path + 'test.txt'
        self.csv_file = path + 'test.csv'
        self.csv_file_40_lines = path + 'test_40.csv'
        self.csv_file_12_lines = path + 'test_12.csv'
        self.csv_file_faulty_1 = path + 'test_faulty_file_1.csv'
        self.csv_file_faulty_2 = path + 'test_faulty_file_2.csv'

    def bind_form_data(self, _file):
        file_data = {'user_list': SimpleUploadedFile(_file.name, _file.read())}
        form = BulkUserUploadForm({}, file_data, user=self.user)
        return form

    def test_clean_invalid_file_type(self):
        with open(self.txt_file) as _file:
            form = self.bind_form_data(_file)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['__all__'][0], 'Please upload a CSV file.')

    def test_clean_exceed_max_file_length(self):
        with open(self.csv_file_40_lines) as _file:
            form = self.bind_form_data(_file)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['__all__'][0], 'Uploaded file should not have more than 30 lines. It has 40.')

    def test_clean_exceed_group_threshold(self):
        with open(self.csv_file_12_lines) as _file:
            form = self.bind_form_data(_file)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['__all__'][0],
                'You are not allowed to create more users than your group threshold. Your group threshold is set to 10.')

    def test_clean_faulty_file_format_1(self):
        with open(self.csv_file_faulty_1) as _file:
            form = self.bind_form_data(_file)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['__all__'][0], 'File line has too many or too few values. Please check file.')

    def test_clean_faulty_file_format_2(self):
        with open(self.csv_file_faulty_2) as _file:
            form = self.bind_form_data(_file)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['__all__'][0], 'File line has too many or too few values. Please check file.')

    def test_clean_duplicate_email(self):
        user = User.objects.create_user('dayo@dziffa.com', 'dayo@dziffa.com', '12345')
        group = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        subscriber = Subscriber.objects.create(user=user, country='GHA', phone_number='0542751610', group=group)

        with open(self.csv_file) as _file:
            form = self.bind_form_data(_file)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['__all__'][0], 'Duplicate email found. dayo@dziffa.com already exists.')
