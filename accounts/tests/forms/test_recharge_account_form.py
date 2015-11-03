from django.conf import settings

from . import FormsTestCase

from ...forms import RechargeAccountForm
from ...helpers import send_api_request

class RechargeAccountFormTest(FormsTestCase):

    def setUp(self, *args, **kwargs):
        super(RechargeAccountFormTest, self).setUp(*args, **kwargs)
        self.data = {'pin': '12345678901234'}

        # Insert stub recharge card
        self.voucher = send_api_request(settings.VOUCHER_STUB_INSERT_URL, self.data)

    def test_clean_short_pin(self):
        data = {'pin': '123456'}
        form = RechargeAccountForm(data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'PINs cannot be shorter than 14 characters.')

    def test_clean_used_voucher(self):
        # Invalidate card
        send_api_request(settings.VOUCHER_INVALIDATE_URL, {'id': self.voucher['id']})

        # Test
        form = RechargeAccountForm(self.data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Voucher has been used.')

    def test_clean_invalid_pin(self):
        data = {'pin': '12345678901235'}
        
        form = RechargeAccountForm(data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Voucher does not exist.')

    def tearDown(self):
        # Delete card
        send_api_request(settings.VOUCHER_STUB_DELETE_URL, self.data)
