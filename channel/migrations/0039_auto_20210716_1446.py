# Generated by Django 3.2.3 on 2021-07-16 14:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0038_auto_20210716_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='time',
        ),
        migrations.AlterField(
            model_name='channel',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='video',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
