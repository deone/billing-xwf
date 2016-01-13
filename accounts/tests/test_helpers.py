from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import Client

from ..helpers import (
    auth_and_login, get_balance, send_api_request
)

from views import ViewsTests
from ..models import RechargeAndUsage

class HelpersTests(ViewsTests):

    def test_auth_and_login_fail(self):
        request = self.factory.get(reverse('accounts:login'))
        response = auth_and_login(request, 'b@b.com', '1234')
        self.assertEqual(response, False)

    def test_get_balance_zero(self):
        # User has no recharge entry. Balance should be zero
        self.assertEqual(get_balance(self.user.radcheck), 0)

    def test_get_balance_non_zero(self):
        balance = get_balance(self.user.radcheck)
        card_value = 4
        balance = balance + card_value

        # Recharge user account
        recharge = RechargeAndUsage.objects.create(
            radcheck=self.radcheck,
            amount=card_value,
            balance=balance,
            action='REC',
            activity_id=30
        )

        self.assertEqual(get_balance(self.user.radcheck), 4)

    def test_send_api_request(self):
        data = {'pin': 12345678901234, 'voucher_type': 'STD'}

        response = send_api_request(settings.VOUCHER_STUB_INSERT_URL, data)
        self.assertEqual(response['code'], 200)

        data.update({'voucher_id': response['id']})
        response = send_api_request(settings.VOUCHER_STUB_DELETE_URL, data)
        self.assertEqual(response['code'], 200)
