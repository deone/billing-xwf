# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20151027_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesspoint',
            name='group',
            field=models.ForeignKey(default=1, to='accounts.GroupAccount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='phone_number',
            field=models.CharField(default=1, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
            preserve_default=False,
        ),
    ]
