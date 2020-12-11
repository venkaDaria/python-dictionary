# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_word_part_speech'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='part_speech',
        ),
        migrations.AddField(
            model_name='chain',
            name='part_speech',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]