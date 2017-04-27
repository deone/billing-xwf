# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_auto_20161114_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupaccount',
            name='bill_group_member',
            field=models.BooleanField(default=False),
        ),
    ]
