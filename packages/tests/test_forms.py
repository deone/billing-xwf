from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Subscriber

from ..models import Package
from ..forms import PackageSubscriptionForm

class PackageSubscriptionFormTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.subscriber = Subscriber.objects.create(user=self.user,
            country='GHA', phone_number='0542751610')

    def test_save(self):
        package = Package.objects.create(package_type='Monthly',
            volume='Unlimited', speed='1.5')

        data = {'package_choice': str(package.pk)}
        packages = [(p.id, p) for p in Package.objects.all()]

        form = PackageSubscriptionForm(data,
            user=self.user, packages=packages)

        form.is_valid()
        subscription = form.save()

        self.assertEqual(subscription.package.package_type,
            package.package_type)
