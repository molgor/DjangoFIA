# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-11 22:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoFIA', '0002_auto_20170811_2239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usgrid100km',
            old_name='xmax',
            new_name='xmaxi',
        ),
        migrations.RenameField(
            model_name='usgrid100km',
            old_name='xmin',
            new_name='xmini',
        ),
        migrations.RenameField(
            model_name='usgrid100km',
            old_name='ymax',
            new_name='ymaxi',
        ),
        migrations.RenameField(
            model_name='usgrid100km',
            old_name='ymin',
            new_name='ymini',
        ),
    ]