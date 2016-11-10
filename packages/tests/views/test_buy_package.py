from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages

from accounts.models import RechargeAndUsage
from accounts.tests.views import ViewsTests

from ...views import buy_package
from ...models import Package

class BuyPackageTests(ViewsTests):

    def test_buy_package_get(self):
        self.c.post(reverse('accounts:login'), {'username': '0542751610', 'password': '12345'})
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
        request.session['client_ip'] = '10.8.0.78'
        request.session['login_url'] = u'https://n110.network-auth.com/splash/login?mauth=MMNsInqn8ksWBR7PgbfBkWG8PawzJm1wi4PE9pDEUdU1qFuHtYczZmRJFJ3dD7AJvl9DRppZnJAZOTA7L3KbzaX4WgwU74t5ibpIJBwHJ-eg5RnL4Hct5hs7i1UIRBH6kbeL9X4hlcFLZKvkaV2mpeP_hX9hxs5jGl_C0N6oWtoQtUjskrMcnBaA&continue_url=http%3A%2F%2Fgoogle.com%2F'
        request.session['continue_url'] = 'http://google.com/'
        request.session['ap_tags'] = 'office-accra recently-added'
        request.session['ap_mac'] = '00:18:0a:f2:de:20'
        request.session['ap_name'] = 'Spectra-HQ-NOC'
        request.session['client_mac'] = '4c:eb:42:ce:6c:3d'
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
        self.assertEqual("Package purchased successfully. <a class='btn btn-primary' href=/captive/?login_url=https://n110.network-auth.com/splash/login?mauth=MMNsInqn8ksWBR7PgbfBkWG8PawzJm1wi4PE9pDEUdU1qFuHtYczZmRJFJ3dD7AJvl9DRppZnJAZOTA7L3KbzaX4WgwU74t5ibpIJBwHJ-eg5RnL4Hct5hs7i1UIRBH6kbeL9X4hlcFLZKvkaV2mpeP_hX9hxs5jGl_C0N6oWtoQtUjskrMcnBaA&continue_url=http%3A%2F%2Fgoogle.com%2F&continue_url=http://google.com/&ap_mac=00:18:0a:f2:de:20&ap_name=Spectra-HQ-NOC&ap_tags=office-accra recently-added&client_mac=4c:eb:42:ce:6c:3d&client_ip=10.8.0.78>Log In To Browse</a>", lst[0].__str__())
