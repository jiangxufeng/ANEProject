# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-07 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0045_auto_20180705_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='nickname',
            field=models.CharField(default='WHUer78504', max_length=20, verbose_name='nickname'),
        ),
    ]
