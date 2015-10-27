# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0008_auto_20151014_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='price',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='grouppackagesubscription',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='packagesubscription',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
