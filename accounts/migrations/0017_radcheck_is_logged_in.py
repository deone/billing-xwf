# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20151222_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='radcheck',
            name='is_logged_in',
            field=models.BooleanField(default=False),
        ),
    ]
