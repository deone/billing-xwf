# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_radcheck_is_logged_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='radcheck',
            name='is_logged_in',
        ),
    ]
