# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0016_auto_20160711_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='volume',
            field=models.CharField(max_length=9, choices=[(b'0.01', b'0.01GB'), (b'1', b'1GB'), (b'3', b'3GB'), (b'5', b'5GB'), (b'8', b'8GB'), (b'10', b'10GB'), (b'12', b'12GB'), (b'15', b'15GB'), (b'20', b'20GB'), (b'25', b'25GB'), (b'Unlimited', b'Unlimited')]),
        ),
    ]
