# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20151008_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='RechargeAndUsage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.SmallIntegerField()),
                ('balance', models.SmallIntegerField()),
                ('action', models.CharField(max_length=3, choices=[(b'', b'Select Action'), (b'REC', b'Recharge'), (b'USG', b'Usage')])),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('subscriber', models.OneToOneField(to='accounts.Subscriber')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
