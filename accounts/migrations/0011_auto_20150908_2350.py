# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20150901_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='date_verified',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
