from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from packages.models import PackageSubscription

from accounts.models import GroupAccount

class GroupAccountPayment(models.Model):
    group = models.ForeignKey(GroupAccount)
    payment_for = models.DateField()
    date = models.DateTimeField(editable=False, default=timezone.now)

class IndividualPayment(models.Model):
    subscription = models.ForeignKey(PackageSubscription)
    token = models.CharField(_('token'), max_length=20)
