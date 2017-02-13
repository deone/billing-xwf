# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_remove_groupaccount_bill_group_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='radpostauth',
            name='message',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
