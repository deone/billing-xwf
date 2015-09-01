# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20150901_2022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accesspoint',
            options={'verbose_name': 'Access Point'},
        ),
        migrations.AlterModelOptions(
            name='groupaccount',
            options={'verbose_name': 'Group Account'},
        ),
        migrations.AlterField(
            model_name='accesspoint',
            name='group',
            field=models.ForeignKey(blank=True, to='accounts.GroupAccount', null=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='group',
            field=models.ForeignKey(blank=True, to='accounts.GroupAccount', null=True),
        ),
    ]
