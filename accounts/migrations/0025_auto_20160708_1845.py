# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20160627_1053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='radcheck',
            old_name='data_usage',
            new_name='data_balance',
        ),
    ]
