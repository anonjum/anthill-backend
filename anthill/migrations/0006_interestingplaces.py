# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-14 14:36
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anthill', '0005_auto_20160814_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterestingPlaces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('postalcode', models.IntegerField()),
                ('municipal', models.CharField(max_length=500)),
                ('coordinate', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]
