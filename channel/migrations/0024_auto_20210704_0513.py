# Generated by Django 3.2.3 on 2021-07-03 23:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0023_alter_video_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='channel_name',
        ),
        migrations.AlterField(
            model_name='video',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 7, 4, 5, 13, 38, 155952)),
        ),
    ]
