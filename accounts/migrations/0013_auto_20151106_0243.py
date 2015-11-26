# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20151106_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesspoint',
            name='group',
            field=models.ForeignKey(blank=True, to='accounts.GroupAccount', null=True),
        ),
    ]
