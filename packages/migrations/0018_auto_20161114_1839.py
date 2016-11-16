# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0017_auto_20160718_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(max_digits=4, decimal_places=2),
        ),
    ]
