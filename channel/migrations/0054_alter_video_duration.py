# Generated by Django 3.2.3 on 2021-07-17 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0053_video_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.IntegerField(blank=True),
        ),
    ]
