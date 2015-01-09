# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def load_initial_permissions(apps, schema_editor):
    Perm = apps.get_model("kratos", "Perm")
    Perm.objects.get_or_create(name='admin')
    Perm.objects.get_or_create(name='write')
    Perm.objects.get_or_create(name='read')


class Migration(migrations.Migration):

    dependencies = [
        ('kratos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_permissions),
    ]
