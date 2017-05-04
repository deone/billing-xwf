# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0022_auto_20170204_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='speed',
            field=models.CharField(default=b'1.5', max_length=5, choices=[(b'2', b'2Mbps Deluxe'), (b'4', b'4Mbps Supreme')]),
        ),
    ]
