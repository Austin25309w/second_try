# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-25 18:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0005_auto_20180425_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
