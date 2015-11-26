from django.test import SimpleTestCase
from django.conf import settings

from ..templatetags.package_tags import get_item

class PackageTagsTest(SimpleTestCase):
  
    def test_get_item(self):
        speed_name = get_item(settings.SPEED_NAME_MAP, '2')
        volume = get_item(settings.VOLUME_NAME_MAP, 'Unlimited')

        self.assertEqual(speed_name, 'Premiere')
        self.assertEqual(volume, 'Unlimited')
