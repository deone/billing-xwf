from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models

class Payment(models.Model):
    # user_application = models.OneToOneField(UserApplication)
    token = models.CharField(_('token'), max_length=20)
