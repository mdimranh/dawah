# Generated by Django 3.2.3 on 2021-07-16 15:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0040_auto_20210716_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
