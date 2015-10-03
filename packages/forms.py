from django import forms
from django.utils import timezone

from .models import Package, PackageSubscription, compute_stop


packages = [(p.id, p) for p in Package.objects.all()]

class PackageSubscriptionForm(forms.Form):
    package_choice = forms.ChoiceField(choices=packages, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PackageSubscriptionForm, self).__init__(*args, **kwargs)

    def save(self):
        package = Package.objects.get(pk=self.cleaned_data['package_choice'])
        stop = compute_stop(package.package_type)
        subscription = PackageSubscription.objects.create(subscriber=self.user.subscriber, package=package, start=timezone.now(), stop=stop)

        return subscription
