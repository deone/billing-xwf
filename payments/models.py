from django.db import models
from django.utils import timezone

from accounts.models import GroupAccount

class Payment(models.Model):
    group = models.ForeignKey(GroupAccount)
    payment_for = models.DateField()
    date = models.DateTimeField(editable=False, default=timezone.now)
