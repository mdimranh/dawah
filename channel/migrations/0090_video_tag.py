# Generated by Django 3.2.3 on 2021-08-05 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0089_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='tag',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
