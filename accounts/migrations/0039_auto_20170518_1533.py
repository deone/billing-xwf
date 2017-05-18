# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_auto_20170204_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rechargeandusage',
            name='amount',
            field=models.DecimalField(max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='rechargeandusage',
            name='balance',
            field=models.DecimalField(max_digits=8, decimal_places=2),
        ),
    ]
