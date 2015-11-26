# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_rechargeandusage_activity_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rechargeandusage',
            name='balance',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
