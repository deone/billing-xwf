from django.contrib.auth.models import AnonymousUser, User

from . import FormsTestCase

from ...forms import CreateUserForm

class CreateUserFormTest(FormsTestCase):

    def setUp(self, *args, **kwargs):
        super(CreateUserFormTest, self).setUp(*args, **kwargs)
        self.data = {
              'username': '0542751610',
              'password': '12345',
              'confirm_password': '12345'
            }

    def test_clean_duplicate_user(self):
        User.objects.create_user('0542751610', '0542751610', '12345')

        form = CreateUserForm(self.data, user=AnonymousUser)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'User already exists')

    def test_clean_password_mismatch(self):
        # Set confirm password field to a different value
        data = self.data
        data['confirm_password'] = '54321'

        form = CreateUserForm(data, user=AnonymousUser)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Passwords do not match')
        
    def test_clean_max_user_count_reached(self):
        # Set group threshold to 1
        self.group.max_no_of_users = 1
        self.group.save()

        form = CreateUserForm(self.data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['__all__'][0].startswith(
          'You are not allowed to create more users than your group threshold.'
          ))

    def test_save(self):
        # Set subscriber as group admin
        self.subscriber.is_group_admin = True
        self.subscriber.save()

        form = CreateUserForm(self.data, user=self.user)
        form.is_valid()
        new_user = form.save()

        self.assertEqual(new_user.subscriber.group.name, self.group.name)
        self.assertEqual(new_user.subscriber.phone_number, '+233542751610')