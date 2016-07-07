from django.db import models
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

from accounts.models import (Subscriber, GroupAccount, Radcheck)
from utils import check_data_balance

class Package(models.Model):
    package_type = models.CharField(max_length=7, choices=settings.PACKAGE_TYPES)
    volume = models.CharField(max_length=9, choices=settings.VOLUME_CHOICES)
    speed = models.CharField(max_length=5, choices=settings.SPEED_CHOICES, default='1.5')
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%s %s %s%s" % (settings.SPEED_NAME_MAP[self.speed],
            self.package_type, self.volume, 'GB')

class InstantVoucher(models.Model):
    radcheck = models.ForeignKey(Radcheck)
    package = models.ForeignKey(Package)

def compute_stop(start, package_type):
    return start + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[package_type])

class AbstractPackageSubscription(models.Model):
    # Add date of purchase
    package = models.ForeignKey(Package)
    start = models.DateTimeField(default=timezone.now) # do we need this default?
    stop = models.DateTimeField(blank=True, null=True, help_text="The time this subscription expires. You are not allowed to set this.")
    purchase_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def is_valid(self, now=timezone.now()):
        stop_date_in_future = self.stop > now
        has_data_left = check_data_balance(self)

        if stop_date_in_future and has_data_left:
            return True

class PackageSubscription(AbstractPackageSubscription):
    radcheck = models.ForeignKey(Radcheck)

    class Meta:
        verbose_name = "Package Subscription"
        ordering = ['-stop'] 

    def __str__(self):
        return "%s %s %s" % (self.radcheck.username, self.package.package_type, self.stop.strftime('%B %d %Y, %I:%M%p'))

class GroupPackageSubscription(AbstractPackageSubscription):
    group = models.ForeignKey(GroupAccount)

    class Meta:
        verbose_name = "Group Package Subscription"
        ordering = ['-stop'] 

    def __str__(self):
        return "%s %s %s" % (self.group.name, self.package.package_type, self.stop.strftime('%B %d %Y, %I:%M%p'))
