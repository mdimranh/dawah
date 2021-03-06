# Generated by Django 3.2.3 on 2021-07-17 16:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channel', '0059_alter_video_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='likes',
            field=models.ManyToManyField(related_name='Likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.ManyToManyField(related_name='Views', to=settings.AUTH_USER_MODEL),
        ),
    ]
