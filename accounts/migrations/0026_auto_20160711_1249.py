# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20160708_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radcheck',
            name='data_balance',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
        ),
    ]
