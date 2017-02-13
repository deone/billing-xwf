# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_radpostauth_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='radpostauth',
            name='client_mac',
            field=models.CharField(default='', max_length=17),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='radpostauth',
            name='authdate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
