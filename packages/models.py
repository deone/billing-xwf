from django.db import models
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

from accounts.models import Subscriber, GroupAccount

class Package(models.Model):
    package_type = models.CharField(max_length=7, choices=settings.PACKAGE_TYPES)
    volume = models.CharField(max_length=9, choices=settings.VOLUME_CHOICES)
    speed = models.CharField(max_length=5, choices=settings.SPEED_CHOICES, default='1.5')
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%s %s %s" % (settings.SPEED_NAME_MAP[self.speed],
            self.package_type, settings.VOLUME_NAME_MAP[self.volume])

def compute_stop(start, package_type):
    return start + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[package_type])

class AbstractPackageSubscription(models.Model):
    package = models.ForeignKey(Package)
    start = models.DateTimeField(default=timezone.now) # do we need this default?
    stop = models.DateTimeField(blank=True, null=True, help_text="The time this subscription expires. You are not allowed to set this.")

    class Meta:
        abstract = True

    def is_valid(self, now=timezone.now()):
        return self.stop > now

class PackageSubscription(AbstractPackageSubscription):
    subscriber = models.ForeignKey(Subscriber)

    class Meta:
        verbose_name = "Package Subscription"
        ordering = ['-stop'] 

    def __str__(self):
        return "%s %s %s" % (self.subscriber.user.email, self.package.package_type, self.stop.strftime('%B %d %Y, %I:%M%p'))

class GroupPackageSubscription(AbstractPackageSubscription):
    group = models.ForeignKey(GroupAccount)

    class Meta:
        verbose_name = "Group Package Subscription"
        ordering = ['-stop'] 

    def __str__(self):
        return "%s %s %s" % (self.group.name, self.package.package_type, self.stop.strftime('%B %d %Y, %I:%M%p'))
