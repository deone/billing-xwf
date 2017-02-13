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
        user, user_created = User.objects.get_or_create(
            username=number,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
        )
        subscriber, subscriber_created = Subscriber.objects.get_or_create(
            user=user,
            defaults={
                'country': 'GHA',
                'phone_number': '%s%s' % ('+233', user.username[1:])
            }
        )
        radcheck, radcheck_created = Radcheck.objects.get_or_create(
            user=user,
            defaults={
                'username': user.username,
                'attribute': 'MD5-Password',
                'op': ':=',
                'value': md5_password(password)
            }
        )

        current_subscription = get_current_subscription(user)

        if radcheck_created:
            sms_recipients.append(number)
            purchase_subscription(user, package)
        else:
            # This script should run in a cron job, maybe every day.
            # Purchase new subscription if:
            # - the last free subscription's stop time is in the past.
            # - Zero data balances (before purchasing a subscription) except where
            # current subscription's package is public.
            last_free_subscription = get_last_free_subscription(user)
            if last_free_subscription:
                if last_free_subscription.stop < now:
                    if not current_subscription.package.is_public:
                        zero_data_balance(user)
                    purchase_subscription(user, package)

    if sms_recipients:
        for number in sms_recipients:
            form = PasswordResetSMSForm({'username': number})
            if form.is_valid():
                form.save(sms_template='accounts/sms_create_password.txt', custom_sms_sender='Spectra-XWF')

def get_current_subscription(user):
    try:
        return user.radcheck.packagesubscription_set.all()[0]
    except:
        return None

def get_last_free_subscription(user):
    try:
        return user.radcheck.packagesubscription_set.filter(package__is_public=False)[0]
    except:
        return None

def zero_data_balance(user):
    # Zero data balance and data usage if current subscription is a non-public subscription
    radcheck = user.radcheck
    radcheck.data_balance = 0
    radcheck.data_usage = 0
    radcheck.save()

def purchase_subscription(user, package):
    # Purchase package
    packages = [(p.id, p) for p in Package.objects.filter(is_public=False)]
    form = PackageSubscriptionForm({'package_choice': package.pk}, user=user, packages=packages)
    form.is_valid()
    form.save()

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