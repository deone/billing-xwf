# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_radcheck_is_logged_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radcheck',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
