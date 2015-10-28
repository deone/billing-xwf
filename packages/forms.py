from django import forms

from .models import Package, PackageSubscription, compute_stop

from accounts.models import RechargeAndUsage
from accounts.helpers import get_balance

class PackageSubscriptionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        packages = kwargs.pop('packages')
        self.user = kwargs.pop('user', None)
        super(PackageSubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['package_choice'] = forms.ChoiceField(choices=packages, widget=forms.RadioSelect())

    def clean(self):
        cleaned_data = super(PackageSubscriptionForm, self).clean()
        package = Package.objects.get(pk=cleaned_data.get('package_choice'))

        amount = -package.price
        balance = get_balance(self.user)
        if (balance - package.price) >= 0:
            balance = balance - package.price
        else:
            raise forms.ValidationError('Package price is more than balance.', code='insufficient-funds')

        return (package, balance, amount)

    def save(self):
        package, balance, amount = self.cleaned_data

        RechargeAndUsage.objects.create(
            subscriber=self.user.subscriber,
            amount=amount,
            balance=balance,
            action='USG',
            activity_id=package.pk
        )

        subscription = PackageSubscription.objects.create(subscriber=self.user.subscriber, package=package)
        subscription.stop = compute_stop(subscription.start, package.package_type)
        subscription.save()

        return subscription
