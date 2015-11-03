from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.conf import settings

from ...views import recharge_account
from ...helpers import send_api_request

from . import ViewsTests

class RechargeAccountTests(ViewsTests):

    def test_recharge_account_get(self):
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('accounts:recharge_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'accounts/recharge_account.html')

    def test_recharge_account_post(self):
        data = {'pin': '12345678901234'}

        # Insert stub recharge card
        send_api_request(settings.VOUCHER_STUB_INSERT_URL, data)

        request = self.factory.post(reverse('accounts:recharge_account'), data=data)
        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = recharge_account(request)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), reverse('accounts:recharge_account'))
        self.assertEqual('Account recharged successfully.', lst[0].__str__())

        # Delete stub recharge card
        send_api_request(settings.VOUCHER_STUB_DELETE_URL, data)
