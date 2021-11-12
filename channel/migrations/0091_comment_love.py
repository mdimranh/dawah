# Generated by Django 3.2.3 on 2021-08-08 02:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channel', '0090_video_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='love',
            field=models.ManyToManyField(blank=True, default=None, related_name='loves', to=settings.AUTH_USER_MODEL),
        ),
    ]
