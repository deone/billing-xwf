# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150910_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupaccount',
            name='package',
        ),
        migrations.RemoveField(
            model_name='groupaccount',
            name='package_start_time',
        ),
        migrations.RemoveField(
            model_name='groupaccount',
            name='package_status',
        ),
        migrations.RemoveField(
            model_name='groupaccount',
            name='package_stop_time',
        ),
    ]
