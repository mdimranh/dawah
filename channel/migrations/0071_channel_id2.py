# Generated by Django 3.2.3 on 2021-07-21 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0070_video_id2'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='id2',
            field=models.TextField(default=''),
        ),
    ]
