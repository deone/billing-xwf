from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Radcheck(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        managed = False
        db_table = 'radcheck'

    def __str__(self):
        return self.username

class Subscriber(models.Model):
    user = models.OneToOneField(User)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15) # validators should be a list
