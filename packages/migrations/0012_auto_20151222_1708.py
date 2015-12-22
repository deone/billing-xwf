# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20151221_1316'),
        ('packages', '0011_instantvoucher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packagesubscription',
            name='subscriber',
        ),
        migrations.AddField(
            model_name='packagesubscription',
            name='radcheck',
            field=models.ForeignKey(default=59, to='accounts.Radcheck'),
            preserve_default=False,
        ),
    ]
