from django.test import Client, TestCase
from django.core.urlresolvers import reverse

from packages.models import Package

import json

class ViewsTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.package_one = Package.objects.create(package_type='Daily', volume='3', speed='1.5', price=4)
        self.package_two = Package.objects.create(package_type='Monthly', volume='3', speed='1.5', price=8)

    def check_response(self, response):
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['status'], 'ok')

    def test_packages(self):
        response = self.c.get(reverse('packages:package_list'))
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 200)
        self.assertEqual(len(value['results']), 2)

    def test_insert_vouchers(self):
        response = self.c.post(reverse('packages:insert_vouchers'),
            data={'username': 'aaaa@spectrawireless.com', 'password': 'BBFF5Y', 'package_id': self.package_one.pk})
        value = json.loads(response.content)

        self.assertEqual(value['status'], 'ok')

    def test_insert_stub_get(self):
        response = self.c.get(reverse('packages:insert_stub'))
        self.check_response(response)

    def test_insert_stub_post(self):
        response = self.c.post(reverse('packages:insert_stub'),
            data={'package_type': 'Daily', 'volume': '3', 'speed': '1.5', 'price': 4})
        value = json.loads(response.content)

        self.assertTrue(value.has_key('package_type'))

    def test_delete_stub_get(self):
        response = self.c.get(reverse('packages:delete_stub'))
        self.check_response(response)

    def test_delete_stub_post(self):
        response = self.c.post(reverse('packages:delete_stub'), data={'package_id': self.package_one.pk})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)
