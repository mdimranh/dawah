# Generated by Django 3.2.3 on 2021-07-17 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0046_auto_20210717_0905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='tag',
        ),
    ]
