# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gh_id', models.IntegerField()),
                ('gh_updated_at', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gh_id', models.IntegerField()),
                ('full_name', models.CharField(max_length=256)),
                ('description', models.CharField(default='', max_length=512, blank=True)),
                ('fork', models.BooleanField(default=False)),
                ('is_enterprise', models.BooleanField(default=True)),
                ('html_url', models.URLField()),
                ('gh_updated_at', models.DateTimeField()),
            ],
            options={
                'ordering': ['fork'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gh_id', models.IntegerField()),
                ('url', models.URLField()),
                ('permission', models.CharField(max_length=6)),
                ('slug', models.CharField(max_length=100)),
                ('is_enterprise', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
