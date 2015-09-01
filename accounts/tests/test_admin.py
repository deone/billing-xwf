from django.test import SimpleTestCase

from ..admin import AccountsUserCreationForm, AccountsUserChangeForm

class AdminFormsTest(SimpleTestCase):

    def setUp(self):
        self.help_text = "Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."
    
    def test_accountsusercreationform(self):
        a = AccountsUserCreationForm()
        self.assertEqual(a.fields['username'].help_text, self.help_text)

    def test_accountsuserchangeform(self):
        a = AccountsUserChangeForm()
        self.assertEqual(a.fields['username'].help_text, self.help_text)
