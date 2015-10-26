#coding=utf-8

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils import timezone

class Nas(models.Model):
    nasname = models.CharField(max_length=128)
    shortname = models.CharField(max_length=32, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    ports = models.IntegerField(blank=True, null=True)
    secret = models.CharField(max_length=60)
    server = models.CharField(max_length=64, blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'nas'

class Radacct(models.Model):
    # radacctid = models.BigIntegerField(primary_key=True)
    acctsessionid = models.CharField(max_length=64)
    acctuniqueid = models.CharField(unique=True, max_length=32)
    username = models.CharField(max_length=64)
    groupname = models.CharField(max_length=64)
    realm = models.CharField(max_length=64, blank=True, null=True)
    nasipaddress = models.CharField(max_length=15)
    nasportid = models.CharField(max_length=15, blank=True, null=True)
    nasporttype = models.CharField(max_length=32, blank=True, null=True)
    acctstarttime = models.DateTimeField(blank=True, null=True)
    acctupdatetime = models.DateTimeField(blank=True, null=True)
    acctstoptime = models.DateTimeField(blank=True, null=True)
    acctinterval = models.IntegerField(blank=True, null=True)
    acctsessiontime = models.IntegerField(blank=True, null=True)
    acctauthentic = models.CharField(max_length=32, blank=True, null=True)
    connectinfo_start = models.CharField(max_length=50, blank=True, null=True)
    connectinfo_stop = models.CharField(max_length=50, blank=True, null=True)
    acctinputoctets = models.BigIntegerField(blank=True, null=True)
    acctoutputoctets = models.BigIntegerField(blank=True, null=True)
    calledstationid = models.CharField(max_length=50)
    callingstationid = models.CharField(max_length=50)
    acctterminatecause = models.CharField(max_length=32)
    servicetype = models.CharField(max_length=32, blank=True, null=True)
    framedprotocol = models.CharField(max_length=32, blank=True, null=True)
    framedipaddress = models.CharField(max_length=15)

    class Meta:
        db_table = 'radacct'

class Radgroupcheck(models.Model):
    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radgroupcheck'


class Radgroupreply(models.Model):
    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radgroupreply'


class Radpostauth(models.Model):
    username = models.CharField(max_length=64)
    pass_field = models.CharField(db_column='pass', max_length=64)  # Field renamed because it was a Python reserved word.
    reply = models.CharField(max_length=32)
    authdate = models.DateTimeField()

    class Meta:
        db_table = 'radpostauth'


class Radreply(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radreply'


class Radusergroup(models.Model):
    username = models.CharField(max_length=64)
    groupname = models.CharField(max_length=64)
    priority = models.IntegerField()

    class Meta:
        db_table = 'radusergroup'

class Radcheck(models.Model):
    user = models.OneToOneField(User, null=True)
    username = models.CharField(max_length=64, unique=True)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radcheck'

    def __str__(self):
        return self.username

class GroupAccount(models.Model):
    name = models.CharField(max_length=50)
    max_no_of_users = models.IntegerField(verbose_name="Max. No. of users")

    class Meta:
        verbose_name = "Group Account"

    def __str__(self):
        return self.name

    def active_users_count(self):
        """ Return the number of active users in group. """
        return int(User.objects.filter(subscriber__group__name=self.name).filter(is_active=True).count())

    def available_user_slots_count(self):
        """ Call this only if max_user_count_reached returns False. """
        return int(self.max_no_of_users) - self.active_users_count()

    def max_user_count_reached(self):
        """ Check whether group max. no. of users has been reached. """
        return self.active_users_count() == int(self.max_no_of_users)


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Subscriber(models.Model):
    GHANA = 'GHA'
    NIGERIA = 'NGA'
    IVORY_COAST = 'CIV'
    CONGO_DR = 'COD'
    CAMEROUN = 'CMR'
    ANGOLA = 'AGO'
    GABON = 'GAB'

    COUNTRY_CHOICES = (
        ('', 'Select Country'),
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
    group = models.ForeignKey(GroupAccount, null=True, blank=True)
    is_group_admin = models.BooleanField(default=False, verbose_name="Group Admin Status",
        help_text="Designates whether this user can create other users in the same group.")
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default=GHANA)
    phone_number = models.CharField(null=True, validators=[phone_regex], max_length=15) # validators should be a list
    email_verified = models.BooleanField(default=False, help_text="Designates whether this user has confirmed they own specified email address.")
    date_verified = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class AccessPoint(models.Model):
    PRIVATE = 'PRV'
    PUBLIC = 'PUB'

    STATUS_CHOICES = (
        ('', 'Select Status'),
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
    )

    name = models.CharField(max_length=30, unique=True)
    group = models.ForeignKey(GroupAccount, null=True, blank=True)
    mac_address = models.CharField(max_length=17, unique=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=PRIVATE)

    class Meta:
        verbose_name = "Access Point"

    def allows(self, user):
        if self.status == 'PUB':
            return True # AP is public, all users can connect
        else:
            if user.subscriber.group is not None and self.group is not None: # This ensures we return False even if AP doesn't belong to a group
                if user.subscriber.group == self.group:
                    return True # Users in same group as AP can connect
                else:
                    return False # Users in other groups can not connect to this AP
            return False # AP is private, only users who belong to AP group can connect

    def __str__(self):
        return self.name

class RechargeAndUsage(models.Model):
    RECHARGE = 'REC'
    USAGE = 'USG'

    ACTION_CHOICES = (
        ('', 'Select Action'),
        (RECHARGE, 'Recharge'),
        (USAGE, 'Usage'),
    )

    subscriber = models.ForeignKey(Subscriber)
    amount = models.SmallIntegerField() # Recharges are positive values, usages are negative values
    balance = models.SmallIntegerField() # Stores balance after every recharge or usage activity, we have to fetch last activity's balance to compute this.
    action = models.CharField(max_length=3, choices=ACTION_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    activity_id = models.IntegerField() # This is voucher ID in the case of recharge, and package ID in the case of usage.

    class Meta:
        ordering = ['-date']
