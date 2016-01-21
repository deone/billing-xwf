from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages

from ...models import Subscriber, Radcheck
from ...views import edit_user
from ...forms import EditUserForm
from ...helpers import md5_password

from . import ViewsTests

class EditUserTests(ViewsTests):

    def test_edit_user_get(self):
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})

        user = User.objects.create(email='c@c.com', username='c@c.com', password='12345', is_active=False)
        subscriber = Subscriber.objects.create(user=user, country='GHA')

        response = self.c.get(reverse('accounts:edit_user', kwargs={'pk':user.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], EditUserForm))
        self.assertEqual(response.context['form'].initial['phone_number'], "")

    def test_edit_user_post(self):
        user = User.objects.create(email='d@d.com', username='d@d.com', password='12345', is_active=False)
        subscriber = Subscriber.objects.create(user=user, country='GHA',
            phone_number=Subscriber.COUNTRY_CODES_MAP['GHA'] + '542751610')
        Radcheck.objects.create(
            user=user, username=user.username, attribute='MD5-Password', op=':=', value=md5_password('12345')
        )

        request = self.factory.post(reverse('accounts:edit_user', kwargs={'pk':user.pk}), data={
              'username': 'b@de.com',
              'first_name': 'Ola',
              'last_name': 'Ade',
              'phone_number': '0542751233'
              })

        request.user = self.user

        self.session.process_request(request)
        request.session['referrer'] = 'accounts:users'
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = edit_user(request, pk=user.pk)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        u = User.objects.get(pk=user.pk)
        self.assertEqual(u.email, 'b@de.com')
        self.assertEqual(u.username, 'b@de.com')
        self.assertEqual(u.first_name, 'Ola')
        self.assertEqual(u.last_name, 'Ade')
        self.assertEqual(u.subscriber.phone_number, '+233542751233')
        self.assertEqual(u.radcheck.username, 'b@de.com')

        self.assertEqual(response.status_code, 302)
        self.assertEqual('User changed successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('accounts:users'))
