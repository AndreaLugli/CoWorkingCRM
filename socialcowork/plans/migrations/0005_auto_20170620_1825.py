# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0004_invoice_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date_paid',
            field=models.DateField(blank=True, null=True),
        ),
    ]
