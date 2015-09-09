# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20150908_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='is_group_admin',
            field=models.BooleanField(default=False, help_text=b'Designates whether the user can create other users in the same group', verbose_name=b'Group Admin Status'),
        ),
    ]
