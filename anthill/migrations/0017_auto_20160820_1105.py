# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-20 11:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anthill', '0016_auto_20160820_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_code', models.CharField(max_length=10)),
                ('activist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anthill.Activist')),
            ],
        ),
        migrations.RemoveField(
            model_name='meetup',
            name='activists',
        ),
        migrations.AddField(
            model_name='participation',
            name='meetup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anthill.Meetup'),
        ),
    ]