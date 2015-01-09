# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kratos', '0002_auto_20141203_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='kratos_id',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
    ]
