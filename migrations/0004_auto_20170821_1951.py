# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-21 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoFIA', '0003_auto_20170821_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biomassgroups',
            name='code',
            field=models.IntegerField(db_index=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='biomassgroups',
            name='group',
            field=models.IntegerField(db_index=True, max_length=254),
        ),
    ]