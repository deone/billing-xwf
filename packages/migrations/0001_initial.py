# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package_type', models.CharField(max_length=7, choices=[(b'Daily', b'Daily'), (b'Weekly', b'Weekly'), (b'Monthly', b'Monthly')])),
                ('volume', models.CharField(max_length=9, choices=[(b'1', b'1GB'), (b'3', b'3GB'), (b'5', b'5GB'), (b'8', b'8GB'), (b'10', b'10GB'), (b'12', b'12GB'), (b'15', b'15GB'), (b'20', b'20GB'), (b'25', b'25GB'), (b'Unlimited', b'Unlimited')])),
                ('speed', models.CharField(default=b'1.5', max_length=3, choices=[(b'1', b'1Mbps'), (b'1.5', b'1.5Mbps'), (b'2', b'2Mbps')])),
            ],
        ),
    ]
