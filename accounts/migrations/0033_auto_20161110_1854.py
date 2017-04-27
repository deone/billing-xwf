# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_networkparameter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkparameter',
            name='client_mac',
            field=models.CharField(max_length=20),
        ),
    ]
