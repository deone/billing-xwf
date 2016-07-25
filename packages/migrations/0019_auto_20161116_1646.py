# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0018_auto_20161114_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='package_type',
            field=models.CharField(max_length=7, choices=[(b'Twenty', b'Twenty'), (b'Daily', b'Daily'), (b'Weekly', b'Weekly'), (b'Monthly', b'Monthly')]),
        ),
        migrations.AlterField(
            model_name='package',
            name='volume',
            field=models.CharField(max_length=9, choices=[(b'0.05', b'0.05GB'), (b'1', b'1GB'), (b'3', b'3GB'), (b'5', b'5GB'), (b'8', b'8GB'), (b'10', b'10GB'), (b'12', b'12GB'), (b'15', b'15GB'), (b'20', b'20GB'), (b'25', b'25GB'), (b'Unlimited', b'Unlimited')]),
        ),
    ]
