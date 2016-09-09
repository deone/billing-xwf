# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20160725_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupaccount',
            name='data_usage',
            field=models.DecimalField(default=0.0, editable=False, max_digits=8, decimal_places=2),
        ),
        migrations.AddField(
            model_name='radcheck',
            name='data_usage',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='groupaccount',
            name='data_balance',
            field=models.DecimalField(default=0.0, editable=False, max_digits=8, decimal_places=2),
        ),
    ]
