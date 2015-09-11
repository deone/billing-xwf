# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_grouppackagesubscription'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grouppackagesubscription',
            options={'ordering': ['-stop'], 'verbose_name': 'Group Package Subscription'},
        ),
        migrations.AlterField(
            model_name='grouppackagesubscription',
            name='stop',
            field=models.DateTimeField(help_text=b'The time this subscription expires. You are not allowed to set this.', blank=True),
        ),
    ]
