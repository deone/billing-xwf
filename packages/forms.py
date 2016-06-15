from django import forms

from .models import Package
from .helpers import *

class PackageSubscriptionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        packages = kwargs.pop('packages')
        self.user = kwargs.pop('user', None)
        super(PackageSubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['package_choice'] = forms.ChoiceField(choices=packages, widget=forms.RadioSelect())

    def clean(self):
        cleaned_data = super(PackageSubscriptionForm, self).clean()
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

        return create_package(self.user.radcheck, package, start)
