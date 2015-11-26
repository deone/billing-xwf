# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0009_auto_20151027_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='speed',
            field=models.CharField(default=b'1.5', max_length=5, choices=[(b'0.512', b'512Kbps Regular'), (b'1', b'1Mbps Lite'), (b'1.5', b'1.5Mbps Deluxe'), (b'2', b'2Mbps Premiere'), (b'3', b'3Mbps Ultra'), (b'4', b'4Mbps Supreme')]),
        ),
    ]
