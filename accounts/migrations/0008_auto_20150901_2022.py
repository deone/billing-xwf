# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20150901_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('max_user_quantity', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='accesspoint',
            name='group',
            field=models.ForeignKey(to='accounts.GroupAccount', null=True),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='group',
            field=models.ForeignKey(to='accounts.GroupAccount', null=True),
        ),
    ]
