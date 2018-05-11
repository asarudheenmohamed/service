# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-05-06 19:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale_order', '0005_ordertimelapse_pending_time'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderTimelapse',
            new_name='OrderTimeElapsed',
        ),
        migrations.RenameField(
            model_name='ordertimeelapsed',
            old_name='out_delivery_lapse',
            new_name='out_delivery_elapsed',
        ),
        migrations.RenameField(
            model_name='ordertimeelapsed',
            old_name='pending_lapse',
            new_name='pending_elapsed',
        ),
        migrations.RenameField(
            model_name='ordertimeelapsed',
            old_name='processing_lapse',
            new_name='processing_elapsed',
        ),
    ]
