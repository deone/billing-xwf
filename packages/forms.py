from django import forms

from .models import Package, PackageSubscription, compute_stop
from packages.helpers import check_balance_and_subscription, charge_subscriber

class PackageSubscriptionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        packages = kwargs.pop('packages')
        self.user = kwargs.pop('user', None)
        super(PackageSubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['package_choice'] = forms.ChoiceField(choices=packages, widget=forms.RadioSelect())

    def clean(self):
        cleaned_data = super(PackageSubscriptionForm, self).clean()
        package = Package.objects.get(pk=cleaned_data.get('package_choice'))

        return check_balance_and_subscription(self.user.subscriber, package)

    def save(self):
        package = self.cleaned_data['package']
        balance = self.cleaned_data['balance']
        amount = self.cleaned_data['amount']
        start = self.cleaned_data['start']

        charge_subscriber(self.user.subscriber, amount, balance, package)

        subscription = PackageSubscription.objects.create(subscriber=self.user.subscriber, package=package, start=start)
        subscription.stop = compute_stop(subscription.start, package.package_type)
        subscription.save()

        return subscription
