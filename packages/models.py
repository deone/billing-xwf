from django.db import models
from django.conf import settings

class Package(models.Model):
    package_type = models.CharField(max_length=7, choices=settings.PACKAGE_TYPES)
    volume = models.CharField(max_length=9, choices=settings.VOLUME_CHOICES)
    speed = models.CharField(max_length=3, choices=settings.SPEED_CHOICES, default='1.5')

    def __str__(self):
        return "%s %sGB" % (self.package_type, self.volume)
