from django.test import TestCase

from ..models import Package

class PackagesModelsTests(TestCase):

    def setUp(self):
        self.package = Package.objects.create(package_type='Daily', volume='3', speed='1.5')

    def test__str__(self):
        self.assertEqual(self.package.__str__(), 'Daily 3GB')
