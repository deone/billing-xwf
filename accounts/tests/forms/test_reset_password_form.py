from ...models import Radcheck

from ...helpers import md5_password
from ...forms import ResetPasswordForm

from . import FormsTestCase

class ResetPasswordFormTest(FormsTestCase):

    def setUp(self, *args, **kwargs):
        super(ResetPasswordFormTest, self).setUp(*args, **kwargs)
        password = '12345'
        Radcheck.objects.create(
            username=self.user.username, attribute='MD5-Password', op=':=', value=md5_password(password)
        )

    def test_save(self):
        old_password = Radcheck.objects.get(username='e@e.com').value

        data = {'new_password1': '54321', 'new_password2': '54321'}
        form = ResetPasswordForm(self.user, data)
        form.is_valid()
        form.save()

        new_password = Radcheck.objects.get(username='e@e.com').value
        self.assertNotEqual(old_password, new_password)
