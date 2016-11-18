from django import forms

from .models import Package

from accounts.models import Radcheck
from utils import save_subscription, check_balance_and_subscription

def update_cleaned_data(data, dct):
    return data.update(dct)

class PackageSubscriptionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        packages = kwargs.pop('packages')
        self.user = kwargs.pop('user', None)
        super(PackageSubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['package_choice'] = forms.ChoiceField(choices=packages, widget=forms.RadioSelect())

    def clean(self):
        cleaned_data = super(PackageSubscriptionForm, self).clean()
        if cleaned_data == {}:
            raise forms.ValidationError("Please select a package.", code="selection_empty")

        package = Package.objects.get(pk=cleaned_data.get('package_choice'))
        start, amount, balance = check_balance_and_subscription(self.user.radcheck, package) 
        update_cleaned_data(cleaned_data, { 
            'start': start, 'amount': amount, 'balance': balance, 'package': package 
        })

    def save(self):
        package = self.cleaned_data['package']
        start = self.cleaned_data['start']
        amount = self.cleaned_data['amount']
        balance = self.cleaned_data['balance']

        radcheck = Radcheck.objects.get(username__exact=self.user.username)

        return save_subscription(radcheck, package, start, amount=amount, balance=balance, token=None)
