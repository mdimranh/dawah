# Generated by Django 3.2.3 on 2021-07-21 17:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channel', '0072_alter_channel_id2'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, default=None, related_name='Bookmarks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='video',
            name='shares',
            field=models.ManyToManyField(blank=True, default=None, related_name='Shares', to=settings.AUTH_USER_MODEL),
        ),
    ]
