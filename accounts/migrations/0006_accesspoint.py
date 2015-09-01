# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150901_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('mac_address', models.CharField(max_length=17)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
