# Generated by Django 3.2.3 on 2021-07-30 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0083_auto_20210730_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='videolike',
            name='channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='channel.channel'),
        ),
        migrations.AddField(
            model_name='videoview',
            name='channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='channel.channel'),
        ),
    ]
