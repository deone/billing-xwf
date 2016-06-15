# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0013_auto_20160615_1131'),
        ('accounts', '0019_radcheck_is_logged_in'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAccountPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_for', models.DateField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('group', models.ForeignKey(to='accounts.GroupAccount')),
            ],
        ),
        migrations.CreateModel(
            name='IndividualPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=20, verbose_name='token')),
                ('subscription', models.ForeignKey(to='packages.PackageSubscription')),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='group',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
