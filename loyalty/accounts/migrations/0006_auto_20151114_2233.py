# -*- coding: utf-8 -*-
# Generated by Django 1.9b1 on 2015-11-14 22:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20151114_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='mondo_account_id',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='webhook_id',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='mondouser',
            name='access_token',
            field=models.CharField(max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='mondouser',
            name='mondo_user_id',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='mondouser',
            name='refresh_token',
            field=models.CharField(max_length=512, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='loyaltyschemelink',
            unique_together=set([('account', 'scheme')]),
        ),
    ]
