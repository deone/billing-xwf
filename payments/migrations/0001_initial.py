# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20151222_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_for', models.DateField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('group', models.ForeignKey(to='accounts.GroupAccount')),
            ],
        ),
    ]
