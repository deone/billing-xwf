# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20150901_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesspoint',
            name='status',
            field=models.CharField(default=b'PRV', max_length=3, choices=[(b'', b'Select Status'), (b'PRV', b'Private'), (b'PUB', b'Public')]),
        ),
    ]
