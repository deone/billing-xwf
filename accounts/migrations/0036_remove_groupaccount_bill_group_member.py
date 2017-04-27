# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_groupaccount_bill_group_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupaccount',
            name='bill_group_member',
        ),
    ]
