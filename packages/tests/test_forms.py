from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Subscriber, RechargeAndUsage

from ..models import Package
from ..forms import PackageSubscriptionForm

class PackageSubscriptionFormTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.subscriber = Subscriber.objects.create(user=self.user, country='GHA', phone_number='0542751610')
        self.package = Package.objects.create(package_type='Monthly', volume='Unlimited', speed='1.5', price=4)
        self.data = {'package_choice': str(self.package.pk)}
        self.packages = [(p.id, p) for p in Package.objects.all()]
        self.recharge = RechargeAndUsage.objects.create(
            subscriber=self.subscriber,
            amount=3,
            balance=3,
            action='REC',
            activity_id=20
        )

    def test_clean(self):
        form = PackageSubscriptionForm(self.data, user=self.user, packages=self.packages)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Package price is more than balance.')

    def test_save(self):
        self.recharge.balance = 5
        self.recharge.save()
        form = PackageSubscriptionForm(self.data, user=self.user, packages=self.packages)

        form.is_valid()
        subscription = form.save()

        self.assertEqual(subscription.package.package_type, self.package.package_type)
