# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20160624_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='radcheck',
            name='data_usage',
            field=models.IntegerField(default=0),
        ),
    ]
