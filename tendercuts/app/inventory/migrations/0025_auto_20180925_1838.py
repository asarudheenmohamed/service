# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-09-25 13:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_auto_20180921_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifycustomer',
            name='expire_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 25, 20, 0, tzinfo=utc)),
        ),
    ]
