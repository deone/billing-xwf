# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rechargeandusage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rechargeandusage',
            name='subscriber',
            field=models.ForeignKey(to='accounts.Subscriber'),
        ),
    ]
