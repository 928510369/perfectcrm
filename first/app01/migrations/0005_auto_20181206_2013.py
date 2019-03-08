# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-06 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20181206_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default=' ', max_length=64, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default=' ', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='m2m',
            field=models.ManyToManyField(to='app01.Mf'),
        ),
    ]