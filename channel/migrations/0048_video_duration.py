# Generated by Django 3.2.3 on 2021-07-17 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0047_remove_video_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.TextField(default=None),
        ),
    ]
