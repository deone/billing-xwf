# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_auto_20160725_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupaccount',
            name='data_balance',
            field=models.DecimalField(default=0.0, null=True, max_digits=8, decimal_places=2, blank=True),
        ),
    ]
