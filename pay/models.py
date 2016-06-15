from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models

from packages.models import PackageSubscription

class Pay(models.Model):
    subscription = models.ForeignKey(PackageSubscription)
    token = models.CharField(_('token'), max_length=20)
