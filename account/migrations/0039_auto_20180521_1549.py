# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-21 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0038_auto_20180521_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='nickname',
            field=models.CharField(default='WHUer564623', max_length=20, verbose_name='nickname'),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='phone',
            field=models.CharField(default='', max_length=11, verbose_name='phone'),
        ),
    ]