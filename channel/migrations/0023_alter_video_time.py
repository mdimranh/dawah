# Generated by Django 3.2.3 on 2021-07-03 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0022_alter_video_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 7, 3, 18, 39, 37, 892434)),
        ),
    ]
