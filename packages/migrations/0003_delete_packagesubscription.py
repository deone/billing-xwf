# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_packagesubscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PackageSubscription',
        ),
    ]
