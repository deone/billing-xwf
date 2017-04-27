# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20160909_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_ip', models.CharField(max_length=10)),
                ('login_url', models.CharField(max_length=600)),
                ('continue_url', models.CharField(max_length=50)),
                ('ap_tags', models.CharField(max_length=50)),
                ('ap_mac', models.CharField(max_length=20)),
                ('ap_name', models.CharField(max_length=15)),
                ('client_mac', models.CharField(max_length=15)),
                ('logout_url', models.CharField(default=None, max_length=255, null=True)),
                ('subscriber', models.OneToOneField(to='accounts.Subscriber')),
            ],
        ),
    ]
