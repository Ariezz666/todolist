# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('is_finished', models.BooleanField(default=False)),
            ],
        ),
    ]
