# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-02 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_category_direction_level_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='img',
            field=models.ImageField(upload_to='../static/images/Video/', verbose_name='图片'),
        ),
    ]