from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages

from ...forms import CreateUserForm
from ...views import add_user

from . import ViewsTests

class AddUserTests(ViewsTests):
    def test_add_user_get(self):
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('accounts:add_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], CreateUserForm))
        self.assertTemplateUsed(response, 'accounts/add_user.html')

    def test_add_user_post(self):
        request = self.factory.post(reverse('accounts:add_user'),
            data={
              'username': 'b@b.com',
              'password': '12345',
              'first_name': 'Ola',
              'last_name': 'Ade',
              'confirm_password': '12345',
              'country': 'GHA',
              'phone_number': '0542751610'
              })
        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = add_user(request)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('User added successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('accounts:add_user'))
