# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_subscriber_is_group_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupaccount',
            name='max_user_quantity',
        ),
        migrations.AddField(
            model_name='groupaccount',
            name='max_no_of_users',
            field=models.IntegerField(default=10, verbose_name=b'Max. No. of users'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='email_verified',
            field=models.BooleanField(default=False, help_text=b'Designates whether this user has confirmed they own specified email address.'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='is_group_admin',
            field=models.BooleanField(default=False, help_text=b'Designates whether this user can create other users in the same group.', verbose_name=b'Group Admin Status'),
        ),
    ]
