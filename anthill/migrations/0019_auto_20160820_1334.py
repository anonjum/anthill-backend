# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-20 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anthill', '0018_meetup_activists'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participation',
            name='invite_code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([('activist', 'meetup')]),
        ),
    ]