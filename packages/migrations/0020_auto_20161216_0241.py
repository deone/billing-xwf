# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0019_auto_20161116_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='package_type',
            field=models.CharField(max_length=7, choices=[(b'Ten', b'Ten'), (b'Daily', b'Daily'), (b'Weekly', b'Weekly'), (b'Monthly', b'Monthly')]),
        ),
    ]
