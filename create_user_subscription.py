#! /usr/bin/env python

import os
import sys
from datetime import timedelta

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "billing.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from packages.models import Package
from packages.forms import PackageSubscriptionForm
from accounts.helpers import md5_password
from accounts.forms import PasswordResetSMSForm
from accounts.models import Radcheck, Subscriber

# Flow

# New account
# - Create account
# - Get package
# - Create subscription
# - Send sms

# Existing account
# - Get account
# - Get package
# - Check whether existing subscription is valid
# - If subscription is invalid, renew subscription

key = sys.argv[1]
now = timezone.now()
password = 'xxx'

def main():
    if key == 'students':
        package = Package.objects.get(volume='12')
        file = 'students.csv'
    elif key == 'staff':
        package = Package.objects.get(volume='15')
        file = 'staff.csv'

    sms_recipients = []
    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        first_name, last_name, number, email = parse_line(line)
        user = get_or_create_user(number, first_name, last_name, email)
        subscriber = get_or_create_subscriber(user)
        radcheck, created = get_or_create_radcheck(user)
        subscription = get_subscription(user)

        if created:
            sms_recipients.append(number)

        subscription_is_valid = False
        if subscription:
            subscription_is_valid = subscription.stop > now and subscription.has_data_left()

        if created or not subscription_is_valid:
            purchase_subscription(user, package)

        if sms_recipients:
            for number in sms_recipients:
                form = PasswordResetSMSForm({'username': number})
                if form.is_valid():
                    form.save(sms_template='accounts/sms_create_password.txt', custom_sms_sender='Spectra-XWF')

def get_subscription(user):
    try:
        return user.radcheck.packagesubscription_set.all()[0]
    except:
        return None

def purchase_subscription(user, package):
    # Zero data balance and data usage
    radcheck = user.radcheck
    radcheck.data_balance = 0
    radcheck.data_usage = 0
    radcheck.save()

    # Purchase package
    packages = [(p.id, p) for p in Package.objects.filter(is_public=False)]
    form = PackageSubscriptionForm({'package_choice': package.pk}, user=user, packages=packages)
    form.is_valid()
    form.save()

def get_or_create_subscriber(user):
    try:
        subscriber = Subscriber.objects.get(user=user)
    except Subscriber.DoesNotExist:
        subscriber = Subscriber.objects.create(user=user, country='GHA', phone_number='+233' + user.username[1:])

    return subscriber

def get_or_create_radcheck(user):
    try:
        radcheck = Radcheck.objects.get(user=user)
    except Radcheck.DoesNotExist:
        radcheck = Radcheck.objects.create(user=user,
                                    username=user.username,
                                    attribute='MD5-Password',
                                    op=':=',
                                    value=md5_password(password))
        created = True
    else:
        created = False

    return radcheck, created

def get_or_create_user(username, first_name, last_name, email):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )

    return user

def parse_line(line):
    parts = line.split(',')
    length = len(parts)

    if length == 4:
        first_name = parts[0].strip()
        last_name = parts[1].strip()
        number = parts[2].strip()
        email = parts[3].strip()
    elif length == 3 or length == 2:
        name = parts[0].split(' ')
        name.reverse()
        first_name = name[1]
        last_name = name[0]
        number = parts[1].strip()
        try:
            email = parts[2].strip()
        except IndexError:
            email = ''

    return [first_name, last_name, number, email]

if __name__ == '__main__':
    main()