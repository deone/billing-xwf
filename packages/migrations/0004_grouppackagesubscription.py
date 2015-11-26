# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150910_1824'),
        ('packages', '0003_delete_packagesubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPackageSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField(blank=True)),
                ('group', models.ForeignKey(to='accounts.GroupAccount')),
                ('package', models.ForeignKey(to='packages.Package')),
            ],
        ),
    ]
