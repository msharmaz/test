# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-10 18:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
