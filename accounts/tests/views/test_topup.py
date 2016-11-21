from django.core.urlresolvers import reverse

from . import ViewsTests

import json

class TopupTests(ViewsTests):
    def test_topup_get(self):
        response = self.c.get(reverse('accounts:topup_account'))

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content)['status'], 'ok')

    def test_topup_post_200(self):
        response = self.c.post(reverse('accounts:topup_account'),
            data={'phone_number': '0542751610', 'amount': '1', 'serial_no': '000001'})

        value = json.loads(response.content)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 200)
        self.assertEqual(value['message'], 'Account recharge successful.')

    def test_topup_post_500(self):
        response = self.c.post(reverse('accounts:topup_account'),
            data={'phone_number': '0542751611', 'amount': '1', 'serial_no': '000002'})

        value = json.loads(response.content)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 500)
        self.assertEqual(value['message'], 'Account does not exist.')