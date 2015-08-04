# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Radcheck',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radcheck',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('country', models.CharField(choices=[('+233', 'Ghana'), ('+234', 'Nigeria'), ('+225', "Cote d'Ivoire"), ('+243', 'Congo'), ('+237', 'Cameroun'), ('+244', 'Angola'), ('+241', 'Gabon')], max_length=4)),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")], blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
