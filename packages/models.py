from django.db import models
from django.conf import settings
from django.utils import timezone

from accounts.models import (Subscriber, GroupAccount, Radcheck)

import time

def check_data_balance(subscription):
    if hasattr(subscription, 'group'):
        data_balance = subscription.group.data_balance
    else:
        data_balance = subscription.radcheck.data_balance

    if subscription.package.volume != 'Unlimited':
        return data_balance > 0
    return True

class Package(models.Model):
    package_type = models.CharField(max_length=7, choices=settings.PACKAGE_TYPES)
    volume = models.CharField(max_length=9, choices=settings.VOLUME_CHOICES)
    speed = models.CharField(max_length=5, choices=settings.SPEED_CHOICES, default='1.5')
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        if self.volume != 'Unlimited':
            return "%s %s %s%s" % (settings.SPEED_NAME_MAP[self.speed], self.package_type, self.volume, 'GB')
        else:
            return "%s %s %s" % (settings.SPEED_NAME_MAP[self.speed], self.package_type, self.volume)

class InstantVoucher(models.Model):
    radcheck = models.ForeignKey(Radcheck)
    package = models.ForeignKey(Package)

class AbstractPackageSubscription(models.Model):
    package = models.ForeignKey(Package)
    start = models.DateTimeField(default=timezone.now) # do we need this default?
    stop = models.DateTimeField(blank=True, null=True, help_text="The time this subscription expires. You are not allowed to set this.")
    purchase_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def is_valid(self, now=timezone.now()):
        package_stop_time_in_seconds = time.mktime(self.stop.timetuple())
        now_in_seconds = time.mktime(now.timetuple())
        
        stop_date_in_future = package_stop_time_in_seconds > now_in_seconds
        has_data_left = check_data_balance(self)

        return stop_date_in_future and has_data_left

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
