from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import Client

from ..helpers import (
    auth_and_login, get_balance, send_vms_request
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
        self.assertEqual(get_balance(self.user), 0)

    def test_get_balance_non_zero(self):
        balance = get_balance(self.user)
        card_value = 4
        balance = balance + card_value

        # Recharge user account
        recharge = RechargeAndUsage.objects.create(
            subscriber=self.subscriber,
            amount=card_value,
            balance=balance,
            action='REC',
            activity_id=30
        )

        self.assertEqual(get_balance(self.user), 4)

    def test_send_vms_request(self):
        url = settings.VOUCHER_INVALIDATE_URL
        payload = 68
        response = send_vms_request(url, payload)
        self.assertEqual(response['code'], 200)
