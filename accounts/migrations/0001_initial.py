# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('mac_address', models.CharField(max_length=17)),
                ('status', models.CharField(default=b'PRV', max_length=3, choices=[(b'', b'Select Status'), (b'PRV', b'Private'), (b'PUB', b'Public')])),
            ],
            options={
                'verbose_name': 'Access Point',
            },
        ),
        migrations.CreateModel(
            name='GroupAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('max_no_of_users', models.IntegerField(verbose_name=b'Max. No. of users')),
                ('package', models.ForeignKey(to='packages.Package')),
            ],
            options={
                'verbose_name': 'Group Account',
            },
        ),
        migrations.CreateModel(
            name='Nas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nasname', models.CharField(max_length=128)),
                ('shortname', models.CharField(max_length=32, null=True, blank=True)),
                ('type', models.CharField(max_length=30, null=True, blank=True)),
                ('ports', models.IntegerField(null=True, blank=True)),
                ('secret', models.CharField(max_length=60)),
                ('server', models.CharField(max_length=64, null=True, blank=True)),
                ('community', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'nas',
            },
        ),
        migrations.CreateModel(
            name='Radacct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acctsessionid', models.CharField(max_length=64)),
                ('acctuniqueid', models.CharField(unique=True, max_length=32)),
                ('username', models.CharField(max_length=64)),
                ('groupname', models.CharField(max_length=64)),
                ('realm', models.CharField(max_length=64, null=True, blank=True)),
                ('nasipaddress', models.CharField(max_length=15)),
                ('nasportid', models.CharField(max_length=15, null=True, blank=True)),
                ('nasporttype', models.CharField(max_length=32, null=True, blank=True)),
                ('acctstarttime', models.DateTimeField(null=True, blank=True)),
                ('acctupdatetime', models.DateTimeField(null=True, blank=True)),
                ('acctstoptime', models.DateTimeField(null=True, blank=True)),
                ('acctinterval', models.IntegerField(null=True, blank=True)),
                ('acctsessiontime', models.IntegerField(null=True, blank=True)),
                ('acctauthentic', models.CharField(max_length=32, null=True, blank=True)),
                ('connectinfo_start', models.CharField(max_length=50, null=True, blank=True)),
                ('connectinfo_stop', models.CharField(max_length=50, null=True, blank=True)),
                ('acctinputoctets', models.BigIntegerField(null=True, blank=True)),
                ('acctoutputoctets', models.BigIntegerField(null=True, blank=True)),
                ('calledstationid', models.CharField(max_length=50)),
                ('callingstationid', models.CharField(max_length=50)),
                ('acctterminatecause', models.CharField(max_length=32)),
                ('servicetype', models.CharField(max_length=32, null=True, blank=True)),
                ('framedprotocol', models.CharField(max_length=32, null=True, blank=True)),
                ('framedipaddress', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'radacct',
            },
        ),
        migrations.CreateModel(
            name='Radcheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radcheck',
            },
        ),
        migrations.CreateModel(
            name='Radgroupcheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupname', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radgroupcheck',
            },
        ),
        migrations.CreateModel(
            name='Radgroupreply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupname', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radgroupreply',
            },
        ),
        migrations.CreateModel(
            name='Radpostauth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('pass_field', models.CharField(max_length=64, db_column=b'pass')),
                ('reply', models.CharField(max_length=32)),
                ('authdate', models.DateTimeField()),
            ],
            options={
                'db_table': 'radpostauth',
            },
        ),
        migrations.CreateModel(
            name='Radreply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radreply',
            },
        ),
        migrations.CreateModel(
            name='Radusergroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('groupname', models.CharField(max_length=64)),
                ('priority', models.IntegerField()),
            ],
            options={
                'db_table': 'radusergroup',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_group_admin', models.BooleanField(default=False, help_text=b'Designates whether this user can create other users in the same group.', verbose_name=b'Group Admin Status')),
                ('country', models.CharField(default=b'GHA', max_length=3, choices=[(b'', b'Select Country'), (b'GHA', b'Ghana'), (b'NGA', b'Nigeria'), (b'CIV', b"Cote d'Ivoire"), (b'COD', b'Congo DR'), (b'CMR', b'Cameroun'), (b'AGO', b'Angola'), (b'GAB', b'Gabon')])),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('email_verified', models.BooleanField(default=False, help_text=b'Designates whether this user has confirmed they own specified email address.')),
                ('date_verified', models.DateTimeField(null=True, blank=True)),
                ('group', models.ForeignKey(blank=True, to='accounts.GroupAccount', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='accesspoint',
            name='group',
            field=models.ForeignKey(blank=True, to='accounts.GroupAccount', null=True),
        ),
    ]
