# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_auto_20150909_0009'),
        ('accounts', '0013_auto_20150909_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupaccount',
            name='package',
            field=models.ForeignKey(default=1, to='packages.Package'),
            preserve_default=False,
        ),
    ]
