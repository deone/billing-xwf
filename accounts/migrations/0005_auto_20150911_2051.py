# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150911_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radcheck',
            name='username',
            field=models.CharField(unique=True, max_length=64),
        ),
    ]
