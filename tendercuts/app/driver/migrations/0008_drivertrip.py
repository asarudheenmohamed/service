# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0007_auto_20171115_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverTrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('km_traveled', models.FloatField(blank=True, null=True)),
                ('trip_created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('trip_ending_time', models.DateTimeField(blank=True, null=True)),
                ('driver_order', models.ManyToManyField(to='driver.DriverOrder')),
            ],
        ),
    ]
