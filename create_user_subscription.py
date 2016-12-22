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
from accounts.models import Subscriber, Radcheck

key = sys.argv[1]
now = timezone.now()
password = 'xxx'

# Get or create packages (12GB and 15GB)
# For students
student_package, created = Package.objects.get_or_create(
    package_type='Monthly',
    volume='12',
    speed='1.5',
    price=0,
)

# For staff
staff_package, created = Package.objects.get_or_create(
    package_type='Monthly',
    volume='15',
    speed='1.5',
    price=0,
)

file_dict = {'students': 'students.csv', 'staff': 'staff.csv'}
package_dict = {'students': student_package, 'staff': staff_package}

file = file_dict[key]
package = package_dict[key]

with open(file) as f:
    lines = f.readlines()

# For each user entry,
lst = []
for line in lines:
    parts = line.split(',')

    first_name = parts[0].strip()
    last_name = parts[1].strip()
    number = parts[2].strip()
    phone_number = '+233' + number[1:]
    email = parts[3].strip()

    # Get or create user - investigate why get_or_create is throwing IntegrityError here.
    try:
        user = User.objects.get(username=number)
    except User.DoesNotExist:
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=number,
            password=password
            )
        created = True
    else:
        created = False

    # Get or create subscriber,
    subscriber, created = Subscriber.objects.get_or_create(user=user, country='GHA', phone_number=phone_number)

    # Get or create radcheck - use get_or_create here too.
    try:
        radcheck = Radcheck.objects.get(user=user)
    except Radcheck.DoesNotExist:
        radcheck = Radcheck.objects.create(user=user,
                                    username=number,
                                    attribute='MD5-Password',
                                    op=':=',
                                    value=md5_password(password))
        created = True
    else:
        created = False

    # Don't roll-over data
    radcheck.data_balance = 0
    radcheck.save()

    # Purchase package subscription
    packages = [(p.id, p) for p in Package.objects.filter(is_public=False)]
    form = PackageSubscriptionForm({'package_choice': package.pk}, user=user, packages=packages)
    form.is_valid()
    form.save()

    lst.append(number)

# For first run, send link to user phone numbers to change their password
if created:
    for number in lst:
        form = PasswordResetSMSForm({'username': number})
        if form.is_valid():
            form.save(sms_template='accounts/sms_create_password.txt')