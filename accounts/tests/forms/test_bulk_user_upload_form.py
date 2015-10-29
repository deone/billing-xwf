from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from ...models import Subscriber
from ...forms import BulkUserUploadForm

from . import FormsTestCase

import os

class BulkUserUploadFormTest(FormsTestCase):

    def setUp(self, *args, **kwargs):
        super(BulkUserUploadFormTest, self).setUp(*args, **kwargs)
        self.group.max_no_of_users = 10
        self.group.save()

        path = os.path.join(settings.BASE_DIR, 'accounts/tests/test_files/')
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
        subscriber = Subscriber.objects.create(user=user, country='GHA', phone_number='0542751610', group=self.group)

        with open(self.csv_file) as _file:
            form = self.bind_form_data(_file)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['__all__'][0], 'Duplicate email found. dayo@dziffa.com already exists.')
