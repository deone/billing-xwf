# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_radcheck_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesspoint',
            name='mac_address',
            field=models.CharField(unique=True, max_length=17),
        ),
        migrations.AlterField(
            model_name='accesspoint',
            name='name',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]
