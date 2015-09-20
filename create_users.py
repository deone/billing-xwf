#! /usr/bin/env python

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "billing.settings")
django.setup()

from django.contrib.auth.models import User
from accounts.models import Subscriber, Radcheck
from accounts.helpers import md5_password

_file = "emails_.csv"

# We can use python to process the raw data file.

with open(_file, 'r') as f:
    for line in f:
        first_name, last_name, email = line.split(',')
        email = email[:-1]
        password = '12345'
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        Subscriber.objects.create(is_group_admin=False, country='GHA', email_verified=False, user=user)

        Radcheck.objects.create(username=email, attribute='MD5-Password', op=':=', value=md5_password(password))
