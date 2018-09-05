# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-09-05 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0016_auto_20180902_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleGeocode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(db_index=True, max_length=600)),
                ('latitude', models.CharField(max_length=25)),
                ('longitude', models.CharField(max_length=25)),
                ('location_type', models.CharField(max_length=25)),
                ('area', models.FloatField()),
            ],
        ),
    ]
