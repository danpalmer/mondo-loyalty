# -*- coding: utf-8 -*-
# Generated by Django 1.9b1 on 2015-11-15 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20151114_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='loyaltyschemelink',
            name='balance',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]