from django.test import TestCase, SimpleTestCase
from django.core.urlresolvers import reverse
from django.apps import apps

from setup.tests.views.tests import ViewsTests

from .apps import PaymentsConfig

class TestApp(SimpleTestCase):

    def test(self):
        config = apps.get_app_config('payments')
        self.assertEqual(config.name, 'payments')

class PaymentViewsTests(ViewsTests):

    def test_index(self):
        self.login()
        response = self.c.get(reverse('pay:index', kwargs={'pk': self.user_app.pk}))
        self.assertEqual(response.status_code, 302)
