from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse

from ...views import toggle_status
from ...models import Subscriber

from . import ViewsTests

class ToggleStatusTests(ViewsTests):

    def create_user(self, is_active=True):
        user = User.objects.create_user('b@b.com', 'b@b.com', '12345')
        user.is_active = is_active
        user.save()

        return user

    def create_group_user(self, email):
        country = 'GHA'
        if not self.group.max_user_count_reached():
            user = User.objects.create_user(email, email, '12345')
            user.subscriber = Subscriber.objects.create(user=user, group=self.group,
                country=country, phone_number=Subscriber.COUNTRY_CODES_MAP[country] + '555223345')
            user.subscriber.save()

        return user

    def get_user(self, pk):
        return User.objects.get(pk=pk)

    def send_request(self, pk):
        return self.c.get(reverse('accounts:toggle_status', kwargs={'pk':pk}))

    def check_response(self, response):
        self.assertRedirects(response, reverse('accounts:users'))
        self.assertEqual(response.status_code, 302)

    def set_group_group_admin(self):
        """ Set group and group_admin status for user. """
        self.user.subscriber.group = self.group
        self.user.subscriber.is_group_admin = True
        self.user.subscriber.save()

    def create_request(self):
        request = self.factory.get(reverse('accounts:login'))
        request.user = self.user
        self.session.process_request(request)
        request.session['referrer'] = 'accounts:users'
        request.session.save()

        return request

    def test_toggle_status_inactive(self):
        """ Test that user.is_active is set to False. """

        self.set_group_group_admin()

        request = self.create_request()

        user = self.create_user()

        response = toggle_status(request, user.pk)

        deactivated_user = self.get_user(user.pk)

        self.assertFalse(deactivated_user.is_active)
        self.assertEqual(response.get('location'), reverse('accounts:users'))

    def test_toggle_status_active(self):
        """ Test that user.is_active is set to True. """

        self.set_group_group_admin()

        request = self.create_request()

        user = self.create_user(is_active=False)

        response = toggle_status(request, user.pk)

        activated_user = self.get_user(user.pk)

        self.assertTrue(activated_user.is_active)
        self.assertEqual(response.get('location'), reverse('accounts:users'))

    def test_toggle_status_active_max_user_count_reached(self):
        """ Test that group admin is unable to set user.is_active to True if group has reached its max. no of users. """

        self.set_group_group_admin()

        # Log user in, since login is required
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})

        # Create second user. Group admin is the first
        second_user = self.create_group_user('p@p.com')

        # Deactivate second_user to free slot to create another
        second_user.is_active = False
        second_user.save()

        # Create third user.
        third_user = self.create_group_user('s@s.com')

        # Attempt making second_user active.
        request = self.factory.post(reverse('accounts:toggle_status', kwargs={'pk':second_user.pk}))

        request.user = self.user

        self.session.process_request(request)
        request.session['referrer'] = 'accounts:users'
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = toggle_status(request, pk=second_user.pk)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        # Fetch user again so that we can check it
        inactive_user = self.get_user(second_user.pk)

        # Check that user wasn't made active
        # Also check that error message was added to message storage
        self.assertFalse(inactive_user.is_active)
        self.assertTrue(lst[0].__str__().startswith("You are not allowed"))
