# Generated by Django 3.2.3 on 2021-06-30 03:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0016_alter_video_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='playlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='channel.folder'),
        ),
        migrations.AlterField(
            model_name='video',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 6, 30, 9, 59, 38, 424772)),
        ),
    ]
