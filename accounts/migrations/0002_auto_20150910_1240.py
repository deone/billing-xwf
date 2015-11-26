# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupaccount',
            name='package_start_time',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='groupaccount',
            name='package_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groupaccount',
            name='package_stop_time',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
    ]
