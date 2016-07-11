from django import forms

from .models import Package
from .helpers import *

from accounts.models import Radcheck
from utils import get_volume

from decimal import Decimal

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
        balance = self.cleaned_data['balance']
        amount = self.cleaned_data['amount']
        start = self.cleaned_data['start']

        charge_subscriber(self.user.radcheck, amount, balance, package) 

        # Increment data balance
        volume = get_volume(package)
        radcheck = Radcheck.objects.get(username__exact=self.user.username)
        radcheck.data_balance += Decimal(volume)
        radcheck.save()

        return save_subscription(radcheck, package, start)
