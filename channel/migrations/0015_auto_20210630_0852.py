# Generated by Django 3.2.3 on 2021-06-30 02:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0014_auto_20210624_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='logo',
            field=models.ImageField(upload_to='pics/%y'),
        ),
        migrations.AlterField(
            model_name='video',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 6, 30, 8, 52, 42, 922711)),
        ),
    ]
