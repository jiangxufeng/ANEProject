# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-18 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_auto_20181018_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animals',
            name='images',
            field=models.CharField(max_length=1024, null=True, verbose_name='images'),
        ),
    ]