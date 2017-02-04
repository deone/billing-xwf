# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0021_package_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='speed',
            field=models.CharField(default=b'1.5', max_length=5, choices=[(b'4', b'4Mbps Supreme')]),
        ),
        migrations.AlterField(
            model_name='package',
            name='volume',
            field=models.CharField(max_length=9, choices=[(b'0.1', b'0.1GB'), (b'0.3', b'0.3GB'), (b'1', b'1GB'), (b'2', b'2GB'), (b'2.5', b'2.5GB'), (b'6', b'6GB'), (b'12', b'12GB'), (b'15', b'15GB')]),
        ),
    ]
