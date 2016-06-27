# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_radcheck_data_usage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radcheck',
            name='data_usage',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=4),
        ),
    ]
