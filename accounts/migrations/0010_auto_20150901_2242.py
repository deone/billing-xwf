# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def initial_data(apps, schema_editor):
    GroupAccount = apps.get_model("accounts", "GroupAccount")
    GroupAccount.objects.create(name="Closed User Group", max_user_quantity=20)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20150901_2234'),
    ]

    operations = [
        migrations.RunPython(initial_data),
    ]
