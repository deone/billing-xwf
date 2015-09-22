#! /usr/bin/env python

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "billing.settings")
django.setup()

from django.contrib.auth.models import User
from accounts.models import Subscriber, Radcheck
from accounts.helpers import md5_password

_file = "test.csv"

# We can use python to process the raw data file.

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

with open(_file, 'r') as f:
    lines = f.readlines()

for line in lines:
    first_name, last_name, email = line.split(',')
    email = email[:-1]
    password = id_generator()
    user = User.objects.create_user(email, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    group = GroupAccount.objects.get(name__exact="Koforidua Polytechnic")

    Subscriber.objects.create(group=group, is_group_admin=False, country='GHA', email_verified=False, user=user)

    Radcheck.objects.create(user=user, username=email, attribute='MD5-Password', op=':=', value=md5_password(password))

    with open('done.csv', 'a') as f:
        f.write(email + ',' + password)
