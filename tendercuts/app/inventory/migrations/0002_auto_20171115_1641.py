# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-15 11:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifycustomer',
            old_name='customer_id',
            new_name='customer',
        ),
    ]
