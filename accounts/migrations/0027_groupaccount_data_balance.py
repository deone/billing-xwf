# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20160711_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupaccount',
            name='data_balance',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
        ),
    ]
