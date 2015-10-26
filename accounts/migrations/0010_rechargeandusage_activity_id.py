# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20151025_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='rechargeandusage',
            name='activity_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
