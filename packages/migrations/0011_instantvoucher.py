# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20151221_1040'),
        ('packages', '0010_auto_20151125_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstantVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package', models.ForeignKey(to='packages.Package')),
                ('radcheck', models.ForeignKey(to='accounts.Radcheck')),
            ],
        ),
    ]
