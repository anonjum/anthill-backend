# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-14 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anthill', '0007_activist_facebook_bot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activist',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
