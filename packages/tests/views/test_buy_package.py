from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages

from accounts.models import RechargeAndUsage
from accounts.tests.views import ViewsTests

from ...views import buy_package
from ...models import Package

class BuyPackageTests(ViewsTests):

    def test_buy_package_get(self):
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('packages:buy'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'packages/buy_package.html')

    def test_buy_package_post(self):
        RechargeAndUsage.objects.create(
            radcheck=self.radcheck,
            amount=4,
            balance=4,
            action='REC',
            activity_id=20
        )
        package = Package.objects.create(package_type='Daily', volume='3', speed='1.5', price=4)
        request = self.factory.post(reverse('packages:buy'),
            data={
              'package_choice': str(package.pk)
              })
        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = buy_package(request)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), reverse('packages:buy'))
        self.assertEqual('Package purchased successfully.', lst[0].__str__())
