# Generated by Django 3.2.3 on 2021-07-17 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0056_alter_video_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='folder',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
