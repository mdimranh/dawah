# Generated by Django 3.2.3 on 2021-07-16 14:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0039_auto_20210716_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='video',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
