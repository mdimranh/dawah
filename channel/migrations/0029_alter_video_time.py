# Generated by Django 3.2.3 on 2021-07-04 10:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0028_alter_video_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 7, 4, 16, 45, 56, 883332)),
        ),
    ]
