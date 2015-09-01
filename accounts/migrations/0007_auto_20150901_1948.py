# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def initial_data(apps, schema_editor):
    AccessPoint = apps.get_model("accounts", "AccessPoint")
    AccessPoint.objects.create(name="Djungle HQ 02", mac_address="00:18:0A:F2:DE:20")

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_accesspoint'),
    ]

    operations = [
        migrations.RunPython(initial_data),
    ]
