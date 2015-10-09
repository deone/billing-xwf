# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0006_packagesubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouppackagesubscription',
            name='stop',
            field=models.DateTimeField(help_text=b'The time this subscription expires. You are not allowed to set this.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='packagesubscription',
            name='stop',
            field=models.DateTimeField(help_text=b'The time this subscription expires. You are not allowed to set this.', null=True, blank=True),
        ),
    ]
