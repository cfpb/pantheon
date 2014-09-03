# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('full_name', models.CharField(max_length=256)),
                ('description', models.CharField(default=b'', max_length=512, blank=True)),
                ('fork', models.BooleanField()),
                ('enterprise', models.BooleanField(default=True)),
                ('html_url', models.URLField()),
                ('gh_updated_at', models.DateTimeField()),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
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
                ('enterprise', models.BooleanField(default=True)),
                ('members', models.ManyToManyField(related_name=b'teams', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='repo',
            name='teams',
            field=models.ManyToManyField(related_name=b'repositories', to='github.Team'),
            preserve_default=True,
        ),
    ]
