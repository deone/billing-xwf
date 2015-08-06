#coding=utf-8

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Radcheck(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        # For tests involving models with managed=False, it’s up to you to
        # ensure the correct tables are created as part of the test setup.
        managed = False
        db_table = 'radcheck'

    def __str__(self):
        return self.username

class Subscriber(models.Model):
    GHANA = 'GHA'
    NIGERIA = 'NGA'
    IVORY_COAST = 'CIV'
    CONGO_DR = 'COD'
    CAMEROUN = 'CMR'
    ANGOLA = 'AGO'
    GABON = 'GAB'

    COUNTRY_CHOICES = (
        (GHANA, 'Ghana'),
        (NIGERIA, 'Nigeria'),
        (IVORY_COAST, "Cote d'Ivoire"),
        (CONGO_DR, 'Congo DR'),
        (CAMEROUN, 'Cameroun'),
        (ANGOLA, 'Angola'),
        (GABON, 'Gabon'),
    )

    COUNTRY_CODES_MAP = {
        GHANA: '+233',
        NIGERIA: '+234',
        IVORY_COAST: '+225',
        CONGO_DR: '+243',
        CAMEROUN: '+237',
        ANGOLA: '+244',
        GABON: '+241'
    }

    user = models.OneToOneField(User)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default=GHANA)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15) # validators should be a list

    def __str__(self):
        return self.user.username
