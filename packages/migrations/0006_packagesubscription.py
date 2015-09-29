# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_radcheck_user'),
        ('packages', '0005_auto_20150911_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField(help_text=b'The time this subscription expires. You are not allowed to set this.', blank=True)),
                ('package', models.ForeignKey(to='packages.Package')),
                ('subscriber', models.ForeignKey(to='accounts.Subscriber')),
            ],
            options={
                'ordering': ['-stop'],
                'verbose_name': 'Package Subscription',
            },
        ),
    ]
