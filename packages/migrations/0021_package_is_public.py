# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0020_auto_20161216_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
