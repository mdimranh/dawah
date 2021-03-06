# Generated by Django 3.2.3 on 2021-07-17 16:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channel', '0062_auto_20210717_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='likes',
            field=models.ManyToManyField(blank=True, default=None, related_name='Likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='video',
            name='views',
            field=models.ManyToManyField(blank=True, default=None, related_name='Views', to=settings.AUTH_USER_MODEL),
        ),
    ]
