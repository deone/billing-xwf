# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0024_auto_20170530_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='speed',
            field=models.CharField(default=b'1.5', max_length=5, choices=[(b'.256', b'256Kbps'), (b'.512', b'512Kbps'), (b'.768', b'768Kbps'), (b'.896', b'896Kbps'), (b'1', b'1Mbps'), (b'2', b'2Mbps'), (b'4', b'4Mbps')]),
        ),
        migrations.AlterField(
            model_name='package',
            name='volume',
            field=models.CharField(max_length=9, choices=[(b'0.1', b'100MB'), (b'0.2', b'200MB'), (b'0.25', b'250MB'), (b'0.3', b'300MB'), (b'0.35', b'350MB'), (b'0.6', b'600MB'), (b'0.9', b'900MB'), (b'1', b'1GB'), (b'1.5', b'1.5GB'), (b'2', b'2GB'), (b'2.5', b'2.5GB'), (b'3.5', b'3.5GB'), (b'5', b'5GB'), (b'6', b'6GB'), (b'12', b'12GB'), (b'15', b'15GB')]),
        ),
    ]
